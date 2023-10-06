package buttons

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleOpenSelectGroupButton(u *tgbotapi.Update) error {
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	structures, err := settings.Api.GetStructures()
	if err != nil {
		return err
	}

	var page *pages.Page
	if len(structures) == 1 {
		page, err = pages.CreateFacultiesListPage(&cManager, structures[0].Id)
	} else {
		page, err = pages.CreateStructuresListPage(&cManager)
	}
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(editMessageReq(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
