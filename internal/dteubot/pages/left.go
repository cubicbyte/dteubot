package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"math/rand"
	"strconv"
)

func CreateLeftPage(cm *data.ChatDataManager, backButton string) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	// TODO: Finish this
	rand_ := strconv.Itoa(rand.Intn(1e6))

	page := Page{
		Text: lang.Page.LeftNoMore,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backButton),
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Refresh, "open.calls#refresh&rnd="+rand_),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
