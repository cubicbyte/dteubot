package pages

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Page struct {
	Text                  string
	InlineKeyboard        tgbotapi.InlineKeyboardMarkup
	ParseMode             string
	DisableWebPagePreview bool
}

// CreateMessage creates a telegram message request from the page
func (p *Page) CreateMessage(chatId int64) tgbotapi.MessageConfig {
	msg := tgbotapi.NewMessage(chatId, p.Text)
	if len(p.InlineKeyboard.InlineKeyboard) > 0 {
		msg.ReplyMarkup = p.InlineKeyboard
	}
	if p.ParseMode != "" {
		msg.ParseMode = p.ParseMode
	}
	msg.DisableWebPagePreview = p.DisableWebPagePreview
	return msg
}
