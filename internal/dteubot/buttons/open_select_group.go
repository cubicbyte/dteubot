package buttons

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleOpenSelectGroupButton(u *tgbotapi.Update) error {
	cManager := utils.GetChatDataManager(u.FromChat().ID)

	structures, err := settings.Api.GetStructures()
	if err != nil {
		return err
	}

	var page *pages.Page
	if len(structures) == 1 {
		page, err = pages.CreateFacultiesListPage(cManager, structures[0].Id)
	} else {
		page, err = pages.CreateStructuresListPage(cManager)
	}
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
