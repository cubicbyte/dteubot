package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func CreateNotFoundPage(cm *data.ChatDataManager, backButton string) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	page := Page{
		Text: lang.Page.NotFound,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backButton),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
