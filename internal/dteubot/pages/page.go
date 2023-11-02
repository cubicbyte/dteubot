/*
 * Copyright (c) 2022 Bohdan Marukhnenko
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package pages

import (
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
)

// Page represents a telegram page
type Page struct {
	Text                  string
	ReplyMarkup           tgbotapi.InlineKeyboardMarkup
	ParseMode             models.ParseMode
	DisableWebPagePreview bool
}

// CreateMessage creates a telegram message parameters from the page
func (p *Page) CreateMessage(chatId int64) bot.SendMessageParams {
	params := bot.SendMessageParams{
		ChatID:                chatId,
		Text:                  p.Text,
		ParseMode:             p.ParseMode,
		DisableWebPagePreview: p.DisableWebPagePreview,
		ReplyMarkup:           p.ReplyMarkup,
	}
	return params
}

// CreateEditMessage creates a telegram edit message parameters from the page
func (p *Page) CreateEditMessage(chatId int64, messageId int) bot.EditMessageTextParams {
	params := bot.EditMessageTextParams{
		ChatID:                chatId,
		MessageID:             messageId,
		Text:                  p.Text,
		ParseMode:             p.ParseMode,
		DisableWebPagePreview: p.DisableWebPagePreview,
		ReplyMarkup:           p.ReplyMarkup,
	}
	return params
}
