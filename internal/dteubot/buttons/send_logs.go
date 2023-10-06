package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/logging"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSendLogsButton(u *tgbotapi.Update) error {
	// Check if user is admin
	if adm, err := checkAdmin(u); err != nil || !adm {
		return err
	}

	// Send "sending document" action
	action := tgbotapi.NewChatAction(u.CallbackQuery.Message.Chat.ID, tgbotapi.ChatUploadDocument)
	_, err := settings.Bot.Request(action)
	if err != nil {
		return err
	}

	// Send logs
	msg := tgbotapi.NewDocument(u.CallbackQuery.Message.Chat.ID, tgbotapi.FilePath(logging.LogFilePath))
	_, err = settings.Bot.Send(msg)
	if err != nil {
		return err
	}

	// Create "done" alert
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	lang, err := cManager.GetLanguage()
	if err != nil {
		return err
	}

	alert := tgbotapi.NewCallbackWithAlert(u.CallbackQuery.ID, lang.Alert.Done)
	_, err = settings.Bot.Request(alert)
	if err != nil {
		return err
	}

	return nil
}
