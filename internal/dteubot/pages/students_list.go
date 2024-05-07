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
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/sirkon/go-format/v2"
	"strconv"
)

func CreateStudentsListPage(lang i18n.Language, groupId int) (Page, error) {
	// Send error if group is not selected
	if groupId < 0 {
		return CreateInvalidGroupPage(lang)
	}

	// Get group name
	var groupName string

	group, err := groupsCache.GetGroupById(groupId)
	if err != nil {
		if group == nil {
			return Page{}, err
		}
		log.Warningf("Error getting %d group name: %s", groupId, err)
	}
	if group == nil {
		groupId := utils.EscapeMarkdownV2(strconv.Itoa(groupId))
		groupName = format.Formatp(lang.Text.UnknownGroupName, groupId)
	} else {
		groupName = utils.EscapeMarkdownV2(group.Name)
	}

	// Get students
	students, err := api.GetGroupStudents(groupId)
	if err != nil {
		return Page{}, err
	}

	studentsStr := ""
	for i, student := range students {
		studentPos := strconv.Itoa(i + 1)
		name := utils.EscapeMarkdownV2(student.GetFullName())

		studentsStr += "*" + studentPos + "*\\) " + name + "\n"
	}

	// Return page
	pageText := format.Formatm(lang.Page.StudentsList, format.Values{
		"group":    groupName,
		"students": studentsStr,
	})

	page := Page{
		Text: pageText,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.Back,
					CallbackData: "open.more",
				}},
			},
		},
		ParseMode: "MarkdownV2",
	}

	return page, nil
}
