package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleUnsupportedButton(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	lang, err := cManager.GetLanguage()
	if err != nil {
		return err
	}

	// Send alert
	alert := tgbotapi.NewCallbackWithAlert(u.CallbackQuery.ID, lang.Alert.CallbackQueryUnsupported)
	_, err = settings.Bot.Request(alert)
	if err != nil {
		println("test")
		return err
	}

	// Move to menu page
	uManager := data.UserDataManager{UserId: u.CallbackQuery.From.ID}
	page, err := pages.CreateMenuPage(&cManager, &uManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(editMessageReq(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
