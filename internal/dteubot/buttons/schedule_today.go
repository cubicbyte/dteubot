package buttons

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"time"
)

func HandleScheduleTodayButton(u *tgbotapi.Update) error {
	cManager := utils.GetChatDataManager(u.FromChat().ID)

	today := time.Now().In(settings.Location).Format("2006-01-02")
	page, err := pages.CreateSchedulePage(cManager, today)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
