package dteubot

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"time"
)

func handleTomorrowCommand(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.FromChat().ID}

	tomorrow := time.Now().AddDate(0, 0, 1).Format("2006-01-02")
	page, err := pages.CreateSchedulePage(&cManager, tomorrow)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(page.CreateMessage(cManager.ChatId))
	if err != nil {
		return err
	}

	return nil
}
