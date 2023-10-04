package dteubot

import (
	"github.com/cubicbyte/dteubot/internal/db"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/op/go-logging"
	"os"
	"strconv"
)

var (
	Languages map[string]i18n.Language
	Database  db.Database
	log       = logging.MustGetLogger("bot")
)

// Setup sets up all the bot components.
func Setup() {
	log.Info("Setting up bot")

	// Load localization files
	var err error
	Languages, err = i18n.LoadLangs()
	if err != nil {
		log.Fatalf("Error loading languages: %s\n", err)
	}
	log.Infof("Loaded %d languages\n", len(Languages))

	// Connect to the database
	port, _ := strconv.Atoi(os.Getenv("POSTGRES_PORT"))
	Database = db.Database{
		Host:     os.Getenv("POSTGRES_HOST"),
		Port:     port,
		User:     os.Getenv("POSTGRES_USER"),
		Password: os.Getenv("POSTGRES_PASSWORD"),
		Database: os.Getenv("POSTGRES_DB"),
		Ssl:      os.Getenv("POSTGRES_SSL") == "true",
	}

	err = Database.Connect()
	if err != nil {
		log.Fatalf("Error connecting to database: %s\n", err)
	}
	log.Info("Connected to database")
}

// Run starts the bot.
func Run() {

}
