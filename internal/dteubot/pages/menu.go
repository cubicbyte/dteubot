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
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/i18n"
)

func CreateMenuPage(lang i18n.Language, user *data.User) (Page, error) {
	page := Page{
		Text: lang.Page.Menu,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.Schedule,
					CallbackData: "open.schedule.today",
				}},
				{{
					Text:         lang.Button.Settings,
					CallbackData: "open.settings",
				}, {
					Text:         lang.Button.More,
					CallbackData: "open.more",
				}},
			},
		},
		ParseMode: "MarkdownV2",
	}

	// Add admin panel button if the user is admin
	if user.IsAdmin {
		page.ReplyMarkup.InlineKeyboard = append(page.ReplyMarkup.InlineKeyboard, []gotgbot.InlineKeyboardButton{{
			Text:         lang.Button.AdminPanel,
			CallbackData: "open.admin_panel",
		}})
	}

	return page, nil
}
