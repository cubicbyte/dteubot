package dteubot

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/buttons"
	"github.com/cubicbyte/dteubot/internal/dteubot/commands"
	"github.com/cubicbyte/dteubot/internal/dteubot/errorhandler"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/internal/notifier"
	"github.com/cubicbyte/dteubot/pkg/api/cachedapi"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"os"
	"strconv"
	"time"
)

const CachePath = "cache"
const ApiLevelDBPath = CachePath + "/api"
const ApiCachePath = CachePath + "/api.sqlite"
const GroupsCachePath = CachePath + "/groups.csv"
const TeachersListPath = "teachers.csv"

var log = logging.MustGetLogger("Bot")

// Setup sets up all the Bot components.
func Setup() {
	log.Info("Setting up Bot")

	// Create required directories
	if err := os.Mkdir(CachePath, 0755); err != nil && !os.IsExist(err) {
		log.Fatalf("Error creating cache directory: %s\n", err)
	}

	// Set up the time zone
	var err error
	settings.Location, err = time.LoadLocation("Europe/Kiev")
	if err != nil {
		log.Fatalf("Error loading time zone: %s\n", err)
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
	settings.Api, err = cachedapi.New(
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
	settings.Languages, err = i18n.LoadLangs()
	if err != nil {
		log.Fatalf("Error loading languages: %s\n", err)
	}
	log.Infof("Loaded %d languages\n", len(settings.Languages))

	// Connect to the database
	port, _ := strconv.Atoi(os.Getenv("POSTGRES_PORT"))
	data.SetupCache()
	settings.Db = &data.Database{
		Host:     os.Getenv("POSTGRES_HOST"),
		Port:     port,
		User:     os.Getenv("POSTGRES_USER"),
		Password: os.Getenv("POSTGRES_PASSWORD"),
		Database: os.Getenv("POSTGRES_DB"),
		Ssl:      os.Getenv("POSTGRES_SSL") == "true",
	}
	if err := settings.Db.Connect(); err != nil {
		log.Fatalf("Error connecting to database: %s\n", err)
	}

	// Load the groups cache
	settings.GroupsCache = groupscache.New(GroupsCachePath, settings.Api)
	if err = settings.GroupsCache.Load(); err != nil {
		log.Fatalf("Error loading groups cache: %s\n", err)
	}

	// Load the teachers list
	settings.TeachersList = &teachers.TeachersList{File: TeachersListPath}
	err = settings.TeachersList.Load()
	if errors.Is(err, os.ErrNotExist) {
		log.Warning("TeachersList list file not found. TeachersList links will not be available.")
		log.Warning("Please create a file teachers.csv using scripts/loadteachers.py script.")
	} else if err != nil {
		log.Fatalf("Error loading teachers list: %s\n", err)
	}

	// Connect to the Telegram API
	log.Info("Connecting to Telegram API")
	settings.Bot, err = tgbotapi.NewBotAPI(os.Getenv("BOT_TOKEN"))
	if err != nil {
		log.Fatal("Error connecting to Telegram API: %s\n", err)
		log.Info("Most likely the bot token is invalid or network is unreachable")
		os.Exit(1)
	}

	log.Infof("Connected to Telegram API as %s\n", settings.Bot.Self.UserName)

	// Set up notifier
	err = notifier.Setup(settings.Db, settings.Api, settings.Bot, settings.Languages)
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
	updates := settings.Bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil && update.CallbackQuery == nil {
			continue
		}

		if err := utils.InitDatabaseRecords(&update); err != nil {
			log.Infof("Error initializing database records: %s\n", err)
			errorhandler.HandleError(err, update)
			continue
		}

		if update.Message != nil {
			if err := commands.HandleCommand(update); err != nil {
				log.Infof("Error handling command: %s\n", err)
				errorhandler.HandleError(err, update)
			}
		}

		if update.CallbackQuery != nil {
			if err := buttons.HandleButton(&update); err != nil {
				log.Infof("Error handling button: %s\n", err)
				errorhandler.HandleError(err, update)
			}
		}

		log.Debug("Update processed")
	}
}