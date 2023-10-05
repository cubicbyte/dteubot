package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func CreateMorePage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	page := Page{
		Text: lang.Page.More,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.CallsSchedule, "open.calls"),
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.TimeLeft, "open.left"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.StudentsList, "open.students_list"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Info, "open.info"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
