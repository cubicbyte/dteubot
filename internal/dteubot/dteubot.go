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
	"errors"
	"fmt"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/errorhandler"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/statistic"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/internal/notifier"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
	"github.com/cubicbyte/dteubot/pkg/api/cachedapi"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/op/go-logging"
	"os"
	"strconv"
	"time"
)

const Location = "Europe/Kyiv"
const CachePath = "cache"
const ApiLevelDBPath = CachePath + "/api"
const ApiCachePath = CachePath + "/api.sqlite"
const GroupsCachePath = CachePath + "/groups.csv"
const TeachersListPath = "teachers.csv"

var log = logging.MustGetLogger("Bot")

var (
	bot          *tgbotapi.BotAPI
	db           *sqlx.DB
	api          api2.IApi
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

	// Connect to the database
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

	// Connect to the Telegram API
	log.Info("Connecting to Telegram API")
	bot, err = tgbotapi.NewBotAPI(os.Getenv("BOT_TOKEN"))
	if err != nil {
		log.Fatal("Error connecting to Telegram API: %s\n", err)
		log.Info("Most likely the bot token is invalid or network is unreachable")
		os.Exit(1)
	}

	log.Infof("Connected to Telegram API as %s\n", bot.Self.UserName)

	// Set up notifier
	err = notifier.Setup(db, api, bot, languages)
	if err != nil {
		log.Fatalf("Error setting up notifier: %s\n", err)
	}
}

// Run starts the Bot.
func Run() {
	log.Info("Starting Bot")

	// Start notifier
	notifier.Scheduler.StartAsync()

	// Start updates loop
	u := tgbotapi.NewUpdate(0)
	u.Timeout = -1
	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil && update.CallbackQuery == nil {
			continue
		}

		chatRepo := data.NewPostgresChatRepository(db)
		userRepo := data.NewPostgresUserRepository(db)

		if err := utils.InitDatabaseRecords(&update, chatRepo, userRepo); err != nil {
			log.Errorf("Error initializing database records: %s\n", err)

			lang, err := utils.GetLang("", languages)
			if err != nil {
				log.Errorf("Error getting language: %s\n", err)
				errorhandler.SendErrorToTelegram(err, bot)
			}

			errorhandler.SendErrorToTelegram(err, bot)
			errorhandler.SendErrorPageToChat(&update, bot, lang)
			continue
		}

		chat, err := chatRepo.GetById(update.FromChat().ID)
		if err != nil {
			log.Errorf("Error getting chat: %s\n", err)
			errorhandler.SendErrorToTelegram(err, bot)
			continue
		}

		lang, err := utils.GetLang(chat.LanguageCode, languages)
		if err != nil {
			log.Errorf("Error getting language: %s\n", err)
			errorhandler.SendErrorToTelegram(err, bot)
			continue
		}

		if update.Message != nil {
			// Handle command
			err := HandleCommand(&update)
			if err != nil {
				errorhandler.HandleError(err, update, bot, lang, chat, chatRepo)
			}

			// Save command to statistics
			if update.Message.Command() != "" {
				err = statistic.LogCommand(
					db,
					update.Message.Chat.ID,
					update.Message.From.ID,
					update.Message.MessageID,
					update.Message.Command(),
				)
				if err != nil {
					errorhandler.HandleError(err, update, bot, lang, chat, chatRepo)
				}
			}
		}

		if update.CallbackQuery != nil {
			// Handle button
			if err := HandleButtonClick(&update); err != nil {
				errorhandler.HandleError(err, update, bot, lang, chat, chatRepo)
			}

			// Save button click to statistics
			err := statistic.LogButtonClick(
				db,
				update.CallbackQuery.Message.Chat.ID,
				update.CallbackQuery.From.ID,
				update.CallbackQuery.Message.MessageID,
				update.CallbackQuery.Data,
			)
			if err != nil {
				errorhandler.HandleError(err, update, bot, lang, chat, chatRepo)
			}
		}

		log.Debug("Update processed")
	}
}
