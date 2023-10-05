package dteubot

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("bot")

func HandleCommand(update tgbotapi.Update) error {
	log.Infof("Handling message %s\n", update.Message.Text)

	switch update.Message.Command() {
	case "start":
		if err := handleStartCommand(&update); err != nil {
			return err
		}
	case "today", "t":
		if err := handleTodayCommand(&update); err != nil {
			return err
		}
	case "tomorrow":
		if err := handleTomorrowCommand(&update); err != nil {
			return err
		}
	case "left", "l":
		if err := handleLeftCommand(&update); err != nil {
			return err
		}
	case "calls", "c":
		if err := handleCallsCommand(&update); err != nil {
			return err
		}
	case "settings":
		if err := handleSettingsCommand(&update); err != nil {
			return err
		}
	case "lang", "language":
		if err := handleLanguageCommand(&update); err != nil {
			return nil
		}
	case "group", "g", "select":
		if err := handleGroupCommand(&update); err != nil {
			return err
		}
	case "":
		// Not a command
	default:
		// Not our command
	}

	return nil
}
