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

func CreateFacultiesListPage(lang i18n.Language, structureId int, scheduleType ScheduleType) (Page, error) {
	faculties, err := api.GetFaculties(structureId)
	if err != nil {
		return Page{}, err
	}

	structures, err := api.GetStructures()
	if err != nil {
		return Page{}, err
	}

	// Create back button: if structures list <= 1, go back to menu, else go back to structures list
	var backButton gotgbot.InlineKeyboardButton
	if len(structures) <= 1 {
		backButton = gotgbot.InlineKeyboardButton{
			Text:         lang.Button.Back,
			CallbackData: "open.schedule_selection",
		}
	} else {
		backButton = gotgbot.InlineKeyboardButton{
			Text:         lang.Button.Back,
			CallbackData: "select.schedule_type&t=" + string(scheduleType),
		}
	}

	buttons := make([][]gotgbot.InlineKeyboardButton, len(faculties)+1)
	buttons[0] = []gotgbot.InlineKeyboardButton{backButton}

	for i, faculty := range faculties {
		query := "sel_faculty#id=" + strconv.Itoa(faculty.Id) +
			"&sid=" + strconv.Itoa(structureId) +
			"&t=" + string(scheduleType)
		buttons[i+1] = []gotgbot.InlineKeyboardButton{{
			Text:         faculty.FullName,
			CallbackData: query,
		}}
	}

	page := Page{
		Text:        lang.Page.FacultySelection,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{InlineKeyboard: buttons},
		ParseMode:   "MarkdownV2",
	}

	return page, nil
}
