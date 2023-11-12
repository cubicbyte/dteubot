/*
 * Copyright (c) 2022 Bohdan Marukhnenko
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package dteubot

import (
	"context"
	"errors"
	"fmt"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/PaulSonOfLars/gotgbot/v2/ext/handlers"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/errorhandler"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/statistics"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/internal/notifier"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
	"github.com/cubicbyte/dteubot/pkg/api/cachedapi"
	"github.com/go-co-op/gocron"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/op/go-logging"
	"net/http"
	"os"
	"strconv"
	"strings"
	"time"
)

const Location = "Europe/Kyiv"
const CachePath = "cache"
const ChatsDirPath = "chats"
const UsersDirPath = "users"
const ApiLevelDBPath = CachePath + "/api"
const ApiCachePath = CachePath + "/api.sqlite"
const GroupsCachePath = CachePath + "/groups.csv"
const TeachersListPath = "teachers.csv"

var log = logging.MustGetLogger("Bot")

var (
	bot          *gotgbot.Bot
	updater      *ext.Updater
	db           *sqlx.DB
	api          api2.IApi
	chatRepo     data.ChatRepository
	userRepo     data.UserRepository
	statLogger   statistics.Logger
	scheduler    *gocron.Scheduler
	languages    map[string]i18n.Language
	groupsCache  *groupscache.Cache
	teachersList *teachers.TeachersList
)

// Setup sets up all the Bot components.
func Setup() {
	log.Info("Setting up Bot")

	// Set timezone
	loc, err := time.LoadLocation(Location)
	if err != nil {
		log.Fatalf("Error loading time zone: %s\n", err)
	}
	time.Local = loc

	// Create required directories
	if err := os.Mkdir(CachePath, 0755); err != nil && !os.IsExist(err) {
		log.Fatalf("Error creating cache directory: %s\n", err)
	}

	// Setup the API
	// Get expiration time
	expires, err := strconv.Atoi(os.Getenv("API_CACHE_EXPIRES"))
	if err != nil {
		log.Fatalf("Error parsing API_CACHE_EXPIRES: %s\n", err)
	}
	timeout, err := strconv.Atoi(os.Getenv("API_REQUEST_TIMEOUT"))
	if err != nil {
		log.Fatalf("Error parsing API_REQUEST_TIMEOUT: %s\n", err)
	}
	api, err = cachedapi.New(
		os.Getenv("API_URL"),
		ApiLevelDBPath,
		ApiCachePath,
		time.Duration(expires)*time.Second,
		time.Duration(timeout)*time.Millisecond,
	)
	if err != nil {
		log.Fatalf("Error setting up API: %s\n", err)
	}

	// Load localization files
	languages, err = i18n.LoadLangs()
	if err != nil {
		log.Fatalf("Error loading languages: %s\n", err)
	}
	log.Infof("Loaded %d languages\n", len(languages))

	// Setup the database
	switch os.Getenv("DATABASE_TYPE") {
	case "postgres":
		var ssl string
		if os.Getenv("POSTGRES_SSL") == "true" {
			ssl = "require"
		} else {
			ssl = "disable"
		}

		connStr := fmt.Sprintf("user=%s password=%s host=%s port=%s dbname=%s sslmode=%s",
			os.Getenv("POSTGRES_USER"),
			os.Getenv("POSTGRES_PASSWORD"),
			os.Getenv("POSTGRES_HOST"),
			os.Getenv("POSTGRES_PORT"),
			os.Getenv("POSTGRES_DB"),
			ssl,
		)
		db, err = sqlx.Connect("postgres", connStr)
		if err != nil {
			log.Fatalf("Error connecting to database: %s\n", err)
		}

		chatRepo = data.NewPostgresChatRepository(db)
		userRepo = data.NewPostgresUserRepository(db)
		statLogger = statistics.NewPostgresLogger(db)

	case "file":
		chatRepo, err = data.NewFileChatRepository(ChatsDirPath)
		if err != nil {
			log.Fatalf("Error setting up chat repository: %s\n", err)
		}
		userRepo, err = data.NewFileUserRepository(UsersDirPath)
		if err != nil {
			log.Fatalf("Error setting up user repository: %s\n", err)
		}
		statLogger, err = statistics.NewFileLogger("statistics")
		if err != nil {
			log.Fatalf("Error setting up statistics logger: %s\n", err)
		}

	default:
		log.Fatalf("Unknown database type: %s\n", os.Getenv("DATABASE_TYPE"))
	}

	// Load the groups cache
	groupsCache = groupscache.New(GroupsCachePath, api)
	if err = groupsCache.Load(); err != nil {
		log.Fatalf("Error loading groups cache: %s\n", err)
	}

	// Load the teachers list
	teachersList = &teachers.TeachersList{File: TeachersListPath}
	err = teachersList.Load()
	if errors.Is(err, os.ErrNotExist) {
		log.Warning("TeachersList list file not found. TeachersList links will not be available.")
		log.Warning("Please create a file teachers.csv using scripts/loadteachers.py script.")
	} else if err != nil {
		log.Fatalf("Error loading teachers list: %s\n", err)
	}

	// Set up error handler
	errorhandler.Setup(languages, chatRepo)

	// Set up the bot
	log.Info("Setting up bot")

	opts := gotgbot.BotOpts{
		DisableTokenCheck: true, // Prevent crash when network is unreachable
		BotClient: &gotgbot.BaseBotClient{
			Client: http.Client{},
			DefaultRequestOpts: &gotgbot.RequestOpts{
				Timeout: gotgbot.DefaultTimeout,
				APIURL:  gotgbot.DefaultAPIURL,
			},
		},
	}

	bot, err = gotgbot.NewBot(os.Getenv("BOT_TOKEN"), &opts)
	if err != nil {
		log.Fatal("Error setting up bot: %s\n", err)
	}

	updater = ext.NewUpdater(&ext.UpdaterOpts{
		Dispatcher: ext.NewDispatcher(&ext.DispatcherOpts{
			Error:       errorhandler.HandleError,
			Panic:       errorhandler.PanicsHandler,
			MaxRoutines: ext.DefaultMaxRoutines,
		}),
	})

	// Add bot update handlers
	anyCommandFilter := func(m *gotgbot.Message) bool {
		return strings.HasPrefix(m.Text, "/")
	}

	anyCallbackFilter := func(cq *gotgbot.CallbackQuery) bool {
		return true
	}

	// Init database records
	updater.Dispatcher.AddHandlerToGroup(handlers.NewMessage(anyCommandFilter, InitDatabaseRecords), -10)
	updater.Dispatcher.AddHandlerToGroup(handlers.NewCallback(anyCallbackFilter, InitDatabaseRecords), -10)
	// Save interaction to statistics
	updater.Dispatcher.AddHandlerToGroup(handlers.NewMessage(anyCommandFilter, CommandStatisticHandler), 10)
	updater.Dispatcher.AddHandlerToGroup(handlers.NewCallback(anyCallbackFilter, ButtonStatisticHandler), 10)

	// Set up notifier
	log.Info("Setting up notifier")
	schedulerCtx := context.TODO()
	scheduler, err = notifier.Setup(schedulerCtx, api, bot, languages, chatRepo)
	if err != nil {
		log.Fatalf("Error setting up notifier: %s\n", err)
	}
}

// Run starts the Bot.
func Run() {
	log.Info("Starting Bot")

	// Start notifier
	scheduler.StartAsync()

	// Start bot
	err := updater.StartPolling(bot, &ext.PollingOpts{
		GetUpdatesOpts: &gotgbot.GetUpdatesOpts{
			Timeout: 10,
		},
	})
	if err != nil {
		log.Fatalf("Error starting polling: %s\n", err)
	}
}
