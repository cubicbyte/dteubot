package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func CreateStructuresListPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	structures, err := settings.Api.GetStructures()
	if err != nil {
		return nil, err
	}

	buttons := make([][]tgbotapi.InlineKeyboardButton, len(structures)+1)
	buttons[0] = tgbotapi.NewInlineKeyboardRow(
		tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu"),
	)

	for i, structure := range structures {
		query := "select.schedule.structure#structureId=" + strconv.Itoa(structure.Id)
		buttons[i+1] = tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(structure.FullName, query),
		)
	}

	page := Page{
		Text:           lang.Page.StructureSelection,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
