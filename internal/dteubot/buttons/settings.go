package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSettingsButton(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	page, err := pages.CreateSettingsPage(&cManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(editMessageReq(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
