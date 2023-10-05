package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
)

func CreateLanguageSelectionPage(cm *data.ChatDataManager, backButton string) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	langsCount := len(settings.Languages)

	buttons := make([][]tgbotapi.InlineKeyboardButton, langsCount+1)
	buttons[langsCount] = tgbotapi.NewInlineKeyboardRow(
		tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backButton),
		tgbotapi.NewInlineKeyboardButtonData(lang.Button.Menu, "open.menu#from=language"),
	)

	i := 0
	for code, lang := range settings.Languages {
		query := "select.lang#lang=" + code
		buttons[i] = tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(lang.LangName, query),
		)
		i++
	}

	page := Page{
		Text:           format.Formatp(lang.Page.LangSelection, lang.LangName),
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
