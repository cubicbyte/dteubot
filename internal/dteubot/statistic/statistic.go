package statistic

import (
	_ "embed"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/op/go-logging"
)

var (
	//go:embed sql/log_button_click.sql
	logButtonClickQuery string
	//go:embed sql/log_command.sql
	logCommandQuery string
)

var log = logging.MustGetLogger("Statistic")

// LogButtonClick logs a button click to the database for statistic purposes.
func LogButtonClick(chatId int64, userId int64, messageId int, button string) error {
	log.Debug("Logging button click")

	// Truncate button to 64 characters
	if len(button) > 64 {
		button = button[:64]
	}

	_, err := settings.Db.Db.Exec(logButtonClickQuery, chatId, userId, messageId, button)
	return err
}

// LogCommand logs a bot command to the database for statistic purposes.
func LogCommand(chatId int64, userId int64, messageId int, command string) error {
	log.Debug("Logging command")

	// Truncate command to 64 characters
	if len(command) > 64 {
		command = command[:64]
	}

	_, err := settings.Db.Db.Exec(logCommandQuery, chatId, userId, messageId, command)
	return err
}
