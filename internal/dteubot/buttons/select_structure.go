package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func HandleSelectStructureButton(u *tgbotapi.Update) error {
	// Get structureId from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)
	structureId, ok := button.Params["structureId"]
	if !ok {
		return errors.New("no structureId in button data")
	}

	structId, err := strconv.Atoi(structureId)
	if err != nil {
		return err
	}

	// Create page
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}
	page, err := pages.CreateFacultiesListPage(&cManager, structId)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
