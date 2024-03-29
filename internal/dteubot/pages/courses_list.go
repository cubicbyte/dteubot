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

func CreateCoursesListPage(lang i18n.Language, facultyId int, structureId int) (Page, error) {
	courses, err := api.GetCourses(facultyId)
	if err != nil {
		return Page{}, err
	}

	buttons := make([][]gotgbot.InlineKeyboardButton, len(courses)+1)
	backBtnQuery := "select.schedule.structure#structureId=" + strconv.Itoa(structureId)
	buttons[0] = []gotgbot.InlineKeyboardButton{{
		Text:         lang.Button.Back,
		CallbackData: backBtnQuery,
	}}

	for i, course := range courses {
		query := "select.schedule.course#course=" + strconv.Itoa(course.Course) +
			"&facultyId=" + strconv.Itoa(facultyId) +
			"&structureId=" + strconv.Itoa(structureId)
		buttons[i+1] = []gotgbot.InlineKeyboardButton{{
			Text:         strconv.Itoa(course.Course),
			CallbackData: query,
		}}
	}

	page := Page{
		Text:        lang.Page.CourseSelection,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{InlineKeyboard: buttons},
		ParseMode:   "MarkdownV2",
	}

	return page, nil
}
