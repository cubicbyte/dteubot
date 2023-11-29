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
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"strconv"
	"time"
)

const rowSize = 3

func CreateGroupsListPage(lang i18n.Language, facultyId int, course int, structureId int) (Page, error) {
	groupsList, err := api.GetGroups(facultyId, course)
	if err != nil {
		return Page{}, err
	}

	// Save groups to cache
	groups_ := make([]groupscache.Group, len(groupsList))
	now := time.Now().Unix()
	for i, group := range groupsList {
		groups_[i] = groupscache.Group{
			Id:        group.Id,
			Name:      group.Name,
			Course:    group.Course,
			FacultyId: facultyId,
			Updated:   now,
		}
	}

	err = groupsCache.AddGroups(groups_)
	if err != nil {
		return Page{}, err
	}

	// Create back button
	rowsCount := len(groupsList)/rowSize + 1
	if len(groupsList)%rowSize != 0 {
		rowsCount++
	}
	buttons := make([][]gotgbot.InlineKeyboardButton, rowsCount)
	backBtnQuery := "select.schedule.faculty#facultyId=" + strconv.Itoa(facultyId) +
		"&structureId=" + strconv.Itoa(structureId)
	buttons[0] = []gotgbot.InlineKeyboardButton{{
		Text:         lang.Button.Back,
		CallbackData: backBtnQuery,
	}}

	// Create group buttons
	btns := make([]gotgbot.InlineKeyboardButton, len(groupsList))
	for i, group := range groupsList {
		btns[i] = gotgbot.InlineKeyboardButton{
			Text:         group.Name,
			CallbackData: "select.schedule.group#groupId=" + strconv.Itoa(group.Id),
		}
	}

	// Create keyboard rows
	buttons = append(buttons, utils.SplitRows(btns, rowSize)...)

	page := Page{
		Text:        lang.Page.GroupSelection,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{InlineKeyboard: buttons},
		ParseMode:   "MarkdownV2",
	}

	return page, nil
}
