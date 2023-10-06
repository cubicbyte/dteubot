package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleClearLogsButton(u *tgbotapi.Update) error {
	// Check if user is admin
	if adm, err := checkAdmin(u); err != nil || !adm {
		return err
	}

	// TODO: Clear logs

	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	lang, err := cManager.GetLanguage()
	if err != nil {
		return err
	}

	// Create "done" alert
	alert := tgbotapi.NewCallbackWithAlert(u.CallbackQuery.ID, lang.Alert.Done)

	_, err = settings.Bot.Request(alert)
	if err != nil {
		return err
	}

	return nil
}
