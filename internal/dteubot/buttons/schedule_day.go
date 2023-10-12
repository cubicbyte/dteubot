package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleScheduleDayButton(u *tgbotapi.Update) error {
	cManager := utils.GetChatDataManager(u.FromChat().ID)

	// Get date from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)
	date, ok := button.Params["date"]
	if !ok {
		return errors.New("no date in button data")
	}

	page, err := pages.CreateSchedulePage(cManager, date)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
