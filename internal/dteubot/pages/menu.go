package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func CreateMenuPage(cm *data.ChatDataManager, um *data.UserDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	// Get user data
	uData, err := um.GetUserData()
	if err != nil {
		return nil, err
	}

	page := Page{
		Text: lang.Page.Menu,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Schedule, "open.schedule.today"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Settings, "open.settings"),
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.More, "open.more"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	// Add admin panel button if the user is admin
	if uData.IsAdmin {
		page.InlineKeyboard.InlineKeyboard = append(page.InlineKeyboard.InlineKeyboard, tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(lang.Button.AdminPanel, "open.admin_panel"),
		))
	}

	return &page, nil
}
