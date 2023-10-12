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

func HandleSelectCourseButton(u *tgbotapi.Update) error {
	// Get course, facultyId and structureId from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	course, ok := button.Params["course"]
	if !ok {
		return errors.New("no course in button data")
	}
	facultyId, ok := button.Params["facultyId"]
	if !ok {
		return errors.New("no facultyId in button data")
	}
	structureId, ok := button.Params["structureId"]
	if !ok {
		return errors.New("no structureId in button data")
	}

	course_, err := strconv.Atoi(course)
	if err != nil {
		return err
	}
	facId, err := strconv.Atoi(facultyId)
	if err != nil {
		return err
	}
	structId, err := strconv.Atoi(structureId)
	if err != nil {
		return err
	}

	// Create page
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}
	page, err := pages.CreateGroupsListPage(&cManager, facId, course_, structId)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
