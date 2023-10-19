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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
	"strconv"
)

func CreateStudentsListPage(cm *data.ChatDataManager) (*Page, error) {
	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	lang, err := utils.GetChatLang(chatData)
	if err != nil {
		return nil, err
	}

	students, err := settings.Api.GetGroupStudents(chatData.GroupId)
	if err != nil {
		return nil, err
	}

	// Get group name
	var groupName string
	if chatData.GroupId == -1 {
		groupName = lang.Text.NotSelected
	} else {
		group, err := settings.GroupsCache.GetGroup(chatData.GroupId)
		if err != nil {
			if group == nil {
				return nil, err
			}
			log.Warningf("Error getting %d group name: %s", chatData.GroupId, err)
		}
		if group == nil {
			groupId := utils.EscapeText(tgbotapi.ModeMarkdownV2, strconv.Itoa(chatData.GroupId))
			groupName = format.Formatp(lang.Text.UnknownGroupName, groupId)
		} else {
			groupName = utils.EscapeText(tgbotapi.ModeMarkdownV2, group.Name)
		}
	}

	pageText := ""
	for i, student := range students {
		studentPos := strconv.Itoa(i + 1)
		name := utils.EscapeText(tgbotapi.ModeMarkdownV2, student.GetFullName())

		pageText += "*" + studentPos + "*\\) " + name + "\n"
	}

	pageText = format.Formatm(lang.Page.StudentsList, format.Values{
		"group":    groupName,
		"students": pageText,
	})

	page := Page{
		Text: pageText,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.more"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
