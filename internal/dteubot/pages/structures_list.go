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
	"strconv"
)

func CreateStructuresListPage(lang i18n.Language) (Page, error) {
	structures, err := api.GetStructures()
	if err != nil {
		return Page{}, err
	}

	buttons := make([][]gotgbot.InlineKeyboardButton, len(structures)+1)
	buttons[0] = []gotgbot.InlineKeyboardButton{{
		Text:         lang.Button.Back,
		CallbackData: "open.menu#from=group_select",
	}}

	for i, structure := range structures {
		buttons[i+1] = []gotgbot.InlineKeyboardButton{{
			Text:         structure.FullName,
			CallbackData: "select.schedule.structure#structureId=" + strconv.Itoa(structure.Id),
		}}
	}

	page := Page{
		Text:        lang.Page.StructureSelection,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{InlineKeyboard: buttons},
		ParseMode:   "MarkdownV2",
	}

	return page, nil
}
