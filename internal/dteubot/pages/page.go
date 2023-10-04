package pages

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Page struct {
	Text           string
	InlineKeyboard tgbotapi.InlineKeyboardMarkup
	ParseMode      string
}
