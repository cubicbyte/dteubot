package dteubot

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func handleMenuCommand(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.FromChat().ID}
	uManager := data.UserDataManager{UserId: u.SentFrom().ID}

	page, err := pages.CreateMenuPage(&cManager, &uManager)
	if err != nil {
		return err
	}

	msg := tgbotapi.NewMessage(cManager.ChatId, page.Text)
	msg.ReplyMarkup = page.InlineKeyboard
	msg.ParseMode = page.ParseMode
	if _, err := settings.Bot.Send(msg); err != nil {
		return err
	}

	return nil
}
