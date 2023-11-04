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
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
	"time"
)

const rowSize = 3

func CreateGroupsListPage(lang *i18n.Language, facultyId int, course int, structureId int, api2 api.IApi, groups *groupscache.Cache) (*Page, error) {
	groupsList, err := api2.GetGroups(facultyId, course)
	if err != nil {
		return nil, err
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

	err = groups.AddGroups(groups_)
	if err != nil {
		return nil, err
	}

	// Create back button
	rowsCount := len(groupsList)/rowSize + 1
	if len(groupsList)%rowSize != 0 {
		rowsCount++
	}
	buttons := make([][]tgbotapi.InlineKeyboardButton, 1, rowsCount)
	backBtnQuery := "select.schedule.faculty#facultyId=" + strconv.Itoa(facultyId) +
		"&structureId=" + strconv.Itoa(structureId)
	buttons[0] = tgbotapi.NewInlineKeyboardRow(
		tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backBtnQuery),
	)

	// Create group buttons
	btns := make([]tgbotapi.InlineKeyboardButton, len(groupsList))
	for i, group := range groupsList {
		query := "select.schedule.group#groupId=" + strconv.Itoa(group.Id)
		btns[i] = tgbotapi.NewInlineKeyboardButtonData(group.Name, query)
	}

	// Create keyboard rows
	buttons = append(buttons, utils.SplitRows(btns, rowSize)...)

	page := Page{
		Text:           lang.Page.GroupSelection,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
