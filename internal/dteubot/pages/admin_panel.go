package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func CreateAdminPanelPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := utils.GetLang(cm)
	if err != nil {
		return nil, err
	}

	page := Page{
		Text: lang.Page.AdminPanel,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.ClearCache, "admin.clear_cache"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.ClearLogs, "admin.clear_logs"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.GetLogs, "admin.get_logs"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}