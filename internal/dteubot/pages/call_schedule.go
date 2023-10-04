package pages

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
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
		callsText += fmt.Sprintf("`%d)` *%s* `-` *%s*\n", call.Number, call.TimeStart, call.TimeEnd)
	}

	page := Page{
		Text: fmt.Sprintf(lang.Page.CallSchedule, callsText),
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backButton),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
