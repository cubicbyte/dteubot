package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func CreateFacultiesListPage(cm *data.ChatDataManager, structureId int) (*Page, error) {
	lang, err := utils.GetLang(cm)
	if err != nil {
		return nil, err
	}

	faculties, err := settings.Api.GetFaculties(structureId)
	if err != nil {
		return nil, err
	}

	structures, err := settings.Api.GetStructures()
	if err != nil {
		return nil, err
	}

	// Create back button: if structures list <= 1, go back to menu, else go back to structures list
	var backButton tgbotapi.InlineKeyboardButton
	if len(structures) <= 1 {
		// Back button = menu
		backButton = tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu#from=group_select")
	} else {
		// Back button = structures list
		backButton = tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.select_group")
	}

	buttons := make([][]tgbotapi.InlineKeyboardButton, len(faculties)+1)
	buttons[0] = tgbotapi.NewInlineKeyboardRow(backButton)

	for i, faculty := range faculties {
		query := "select.schedule.faculty#facultyId=" + strconv.Itoa(faculty.Id) + "&structureId=" + strconv.Itoa(structureId)
		buttons[i+1] = tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(faculty.FullName, query),
		)
	}

	page := Page{
		Text:           lang.Page.FacultySelection,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
