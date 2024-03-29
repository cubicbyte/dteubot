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
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/sirkon/go-format/v2"
)

func CreateCallSchedulePage(lang i18n.Language, backButton string) (Page, error) {
	calls, err := api.GetCallSchedule()
	if err != nil {
		return Page{}, err
	}

	callsText := ""
	for _, call := range calls {
		callsText += format.Formatp("`$)` *$* `-` *$*\n", call.Number, call.TimeStart, call.TimeEnd)
	}

	page := Page{
		Text: format.Formatp(lang.Page.CallSchedule, callsText),
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.Back,
					CallbackData: backButton,
				}},
			},
		},
		ParseMode: "MarkdownV2",
	}

	return page, nil
}
