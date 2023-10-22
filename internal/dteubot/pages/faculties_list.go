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
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func CreateFacultiesListPage(lang *i18n.Language, structureId int, api2 api.IApi) (*Page, error) {
	faculties, err := api2.GetFaculties(structureId)
	if err != nil {
		return nil, err
	}

	structures, err := api2.GetStructures()
	if err != nil {
		return nil, err
	}

	// Create back button: if structures list <= 1, go back to menu, else go back to structures list
	var backButton tgbotapi.InlineKeyboardButton
	if len(structures) <= 1 {
		// Back button = menu
		backButton = tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu#from=group_select")
	} else {
		// Back button = structures list
		backButton = tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.select_group")
	}

	buttons := make([][]tgbotapi.InlineKeyboardButton, len(faculties)+1)
	buttons[0] = tgbotapi.NewInlineKeyboardRow(backButton)

	for i, faculty := range faculties {
		query := "select.schedule.faculty#facultyId=" + strconv.Itoa(faculty.Id) + "&structureId=" + strconv.Itoa(structureId)
		buttons[i+1] = tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(faculty.FullName, query),
		)
	}

	page := Page{
		Text:           lang.Page.FacultySelection,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
