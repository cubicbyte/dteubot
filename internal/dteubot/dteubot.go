package dteubot

import (
	"github.com/cubicbyte/dteubot/internal/data"
	dteubot "github.com/cubicbyte/dteubot/internal/dteubot/commands"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"os"
	"strconv"
)

var log = logging.MustGetLogger("Bot")

// Setup sets up all the Bot components.
func Setup() {
	log.Info("Setting up Bot")

	// Load localization files
	var err error
	settings.Languages, err = i18n.LoadLangs()
	if err != nil {
		log.Fatalf("Error loading languages: %s\n", err)
	}
	log.Infof("Loaded %d languages\n", len(settings.Languages))

	// Connect to the database
	port, _ := strconv.Atoi(os.Getenv("POSTGRES_PORT"))
	data.DbInstance = &data.Database{
		Host:     os.Getenv("POSTGRES_HOST"),
		Port:     port,
		User:     os.Getenv("POSTGRES_USER"),
		Password: os.Getenv("POSTGRES_PASSWORD"),
		Database: os.Getenv("POSTGRES_DB"),
		Ssl:      os.Getenv("POSTGRES_SSL") == "true",
	}

	err = data.DbInstance.Connect()
	if err != nil {
		log.Fatalf("Error connecting to database: %s\n", err)
	}

	// Connect to the Telegram API
	log.Info("Connecting to Telegram API")
	settings.Bot, err = tgbotapi.NewBotAPI(os.Getenv("BOT_TOKEN"))
	if err != nil {
		log.Fatalf("Error connecting to Telegram API: %s\n", err)
	}

	log.Infof("Connected to Telegram API as %s\n", settings.Bot.Self.UserName)
}

// Run starts the Bot.
func Run() {
	log.Info("Starting Bot")

	u := tgbotapi.NewUpdate(0)
	u.Timeout = -1

	updates := settings.Bot.GetUpdatesChan(u)

	for update := range updates {
		if err := utils.InitDatabaseRecords(&update); err != nil {
			log.Errorf("Error initializing database records: %s\n", err)
			// TODO: Handle error
			continue
		}

		if update.Message != nil {
			if err := dteubot.HandleCommand(update); err != nil {
				log.Errorf("Error handling command: %s\n", err)
				// TODO: Handle error
			}
		}
	}
}
