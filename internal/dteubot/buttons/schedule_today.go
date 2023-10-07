package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"time"
)

func HandleScheduleTodayButton(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	today := time.Now().In(settings.Location).Format("2006-01-02")
	page, err := pages.CreateSchedulePage(&cManager, today)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(editMessageReq(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
