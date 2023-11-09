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

package commands

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
	"time"
)

func HandleGroupCommand(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, chat *data.Chat, chatRepo data.ChatRepository, groups *groupscache.Cache, api2 api.IApi, teachersList *teachers.TeachersList) error {
	// Get group from command arguments
	args := u.Message.CommandArguments()
	if args != "" {
		groupId, err := strconv.Atoi(args)
		if err != nil {
			// User provided group name instead of id
			// Check if group exists
			group, err := groups.GetGroupByName(args)
			if err != nil {
				return err
			}

			if group == nil {
				// Do not set group if it does not exist
				goto CREATE_PAGE
			}

			groupId = group.Id
		}

		// Set chat group
		chat.GroupId = groupId

		// Update chat
		err = chatRepo.Update(chat)
		if err != nil {
			return err
		}

		// Create today's schedule page
		today := time.Now().Format(time.DateOnly)
		page, err := pages.CreateSchedulePage(lang, groupId, today, api2, teachersList)
		return sendPage(page, err, u, bot)
	}

CREATE_PAGE:
	structures, err := api2.GetStructures()
	if err != nil {
		return err
	}

	var page *pages.Page
	if len(structures) == 1 {
		page, err = pages.CreateFacultiesListPage(lang, structures[0].Id, api2)
	} else {
		page, err = pages.CreateStructuresListPage(lang, api2)
	}

	return sendPage(page, err, u, bot)
}
