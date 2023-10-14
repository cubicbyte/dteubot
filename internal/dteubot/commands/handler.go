package commands

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("bot")

func HandleCommand(update tgbotapi.Update) (bool, error) {
	cmd := update.Message.Command()

	// If there is no command, return
	if cmd == "" {
		return false, nil
	}

	log.Infof("Handling message %s\n", update.Message.Text)

	switch cmd {
	case "start":
		if err := handleStartCommand(&update); err != nil {
			return false, err
		}
	case "today", "t":
		if err := handleTodayCommand(&update); err != nil {
			return false, err
		}
	case "tomorrow":
		if err := handleTomorrowCommand(&update); err != nil {
			return false, err
		}
	case "left", "l":
		if err := handleLeftCommand(&update); err != nil {
			return false, err
		}
	case "calls", "c":
		if err := handleCallsCommand(&update); err != nil {
			return false, err
		}
	case "settings":
		if err := handleSettingsCommand(&update); err != nil {
			return false, err
		}
	case "lang", "language":
		if err := handleLanguageCommand(&update); err != nil {
			return false, err
		}
	case "group", "g", "select":
		if err := handleGroupCommand(&update); err != nil {
			return false, err
		}
	default:
		// Not our command
		return false, nil
	}

	return true, nil
}
