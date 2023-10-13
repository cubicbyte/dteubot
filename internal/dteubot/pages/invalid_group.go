package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func CreateInvalidGroupPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := utils.GetLang(cm)
	if err != nil {
		return nil, err
	}

	page := Page{
		Text: lang.Page.InvalidGroup,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.SelectGroup, "open.select_group"),
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Menu, "open.menu"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}