package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
)

func CreateCallSchedulePage(cm *data.ChatDataManager, backButton string) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	calls, err := settings.Api.GetCallSchedule()
	if err != nil {
		return nil, err
	}

	callsText := ""
	for _, call := range calls {
		callsText += format.Formatp("`$)` *$* `-` *$*\n", call.Number, call.TimeStart, call.TimeEnd)
	}

	page := Page{
		Text: format.Formatp(lang.Page.CallSchedule, callsText),
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backButton),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
