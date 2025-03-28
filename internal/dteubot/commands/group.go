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
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"strconv"
	"strings"
	"time"
)

func HandleGroupCommand(bot *gotgbot.Bot, ctx *ext.Context) error {
	// Get chat
	chat, err := chatRepo.GetById(ctx.EffectiveChat.Id)
	if err != nil {
		return err
	}

	lang, err := utils.GetLang(chat.LanguageCode, languages)
	if err != nil {
		return err
	}

	// Get group from command arguments
	if strings.Contains(ctx.EffectiveMessage.Text, " ") {
		arg := strings.SplitN(ctx.EffectiveMessage.Text, " ", 2)[1]
		groupId, err := strconv.Atoi(arg)
		if err != nil {
			// User provided group name instead of id
			// Check if group exists
			group, err := groupsCache.GetGroupByName(arg)
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
		page, err := pages.CreateSchedulePage(lang, groupId, today)
		return sendPage(bot, ctx, page, err)
	}

CREATE_PAGE:
	page, err := pages.CreateScheduleTypeSelectionPage(lang)
	return sendPage(bot, ctx, page, err)
}
