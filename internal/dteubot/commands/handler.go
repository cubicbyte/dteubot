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
	case "today":
	case "tomorrow":
	case "left":
	case "menu":
		if err := handleMenuCommand(&update); err != nil {
			return err
		}
	case "calls":
	case "settings":
	case "lang":
	case "select":
	case "empty_1", "empty_2":
	case "":
	default:
	}

	return nil
}
