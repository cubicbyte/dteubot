package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func CreateNotificationFeatureSuggestionPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	page := Page{
		Text: lang.Page.NotificationFeatureSuggestion,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Text.TryIt, "set.cl_notif#time=15m&state=1&suggestion"),
				tgbotapi.NewInlineKeyboardButtonData(lang.Text.NoThanks, "close_page#page=notification_feature_suggestion"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
