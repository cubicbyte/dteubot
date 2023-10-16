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

// CreateEditMessage creates a telegram edit message request from the page
func (p *Page) CreateEditMessage(chatId int64, messageId int) tgbotapi.EditMessageTextConfig {
	msg := tgbotapi.NewEditMessageTextAndMarkup(chatId, messageId, p.Text, p.InlineKeyboard)
	msg.ParseMode = p.ParseMode
	msg.DisableWebPagePreview = p.DisableWebPagePreview
	return msg
}
