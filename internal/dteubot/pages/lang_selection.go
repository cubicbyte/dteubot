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
	"sort"
)

func CreateLanguageSelectionPage(lang i18n.Language, backButton string) (Page, error) {
	// Get sorted languages
	langsCount := len(languages)
	sortedLangs := make([]string, langsCount)

	i := 0
	for code := range languages {
		sortedLangs[i] = code
		i++
	}

	sort.Strings(sortedLangs)

	// Create buttons
	buttons := make([][]gotgbot.InlineKeyboardButton, langsCount+1)
	buttons[langsCount] = []gotgbot.InlineKeyboardButton{{
		Text:         lang.Button.Back,
		CallbackData: backButton,
	}, {
		Text:         lang.Button.Menu,
		CallbackData: "open.menu#from=language",
	}}

	// Add language buttons
	i = 0
	for _, code := range sortedLangs {
		lang2 := languages[code]
		buttons[i] = []gotgbot.InlineKeyboardButton{{
			Text:         lang2.LangName,
			CallbackData: "select.lang#lang=" + code,
		}}
		i++
	}

	page := Page{
		Text:        format.Formatp(lang.Page.LangSelection, lang.LangName),
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{InlineKeyboard: buttons},
		ParseMode:   "MarkdownV2",
	}

	return page, nil
}
