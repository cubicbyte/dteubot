package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleMenuButton(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}
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
