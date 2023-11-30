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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/sirkon/go-format/v2"
	"strconv"
)

func CreateSettingsPage(lang i18n.Language, chat *data.Chat) (Page, error) {
	// Mark settings as seen
	if !chat.SeenSettings {
		chat.SeenSettings = true
		if err := chatRepo.Update(chat); err != nil {
			return Page{}, err
		}
	}

	// Get group name
	var groupName string
	if chat.GroupId == -1 {
		groupName = lang.Text.NotSelected
	} else {
		group, err := groupsCache.GetGroupById(chat.GroupId)
		if err != nil {
			if group == nil {
				return Page{}, err
			}
			log.Warningf("Error getting %d group name: %s", chat.GroupId, err)
		}
		if group == nil {
			groupId := utils.EscapeMarkdownV2(strconv.Itoa(chat.GroupId))
			groupName = format.Formatp(lang.Text.UnknownGroupName, groupId)
		} else {
			groupName = utils.EscapeMarkdownV2(group.Name)
		}
	}

	// Get classes notification states
	var (
		notif15mNextState      string
		notif1mNextState       string
		notifNextPartNextState string
	)
	if chat.ClassesNotification15m {
		notif15mNextState = "0"
	} else {
		notif15mNextState = "1"
	}
	if chat.ClassesNotification1m {
		notif1mNextState = "0"
	} else {
		notif1mNextState = "1"
	}
	if chat.ClassesNotificationNextPart {
		notifNextPartNextState = "0"
	} else {
		notifNextPartNextState = "1"
	}

	pageText := format.Formatm(lang.Page.Settings, format.Values{
		"group": groupName,
	})

	page := Page{
		Text: pageText,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.SelectGroup,
					CallbackData: "open.select_group",
				}, {
					Text:         lang.Button.SelectLang,
					CallbackData: "open.select_lang",
				}},
				{{
					Text:         format.Formatp(lang.Button.SettingClNotif15m, utils.GetSettingIcon(chat.ClassesNotification15m)),
					CallbackData: "set.cl_notif#time=15m&state=" + notif15mNextState,
				}},
				{{
					Text:         format.Formatp(lang.Button.SettingClNotif1m, utils.GetSettingIcon(chat.ClassesNotification1m)),
					CallbackData: "set.cl_notif#time=1m&state=" + notif1mNextState,
				}},
				{{
					Text:         format.Formatp(lang.Button.SettingClNotifNextPart, utils.GetSettingIcon(chat.ClassesNotificationNextPart)),
					CallbackData: "set.cl_notif_next_part#state=" + notifNextPartNextState,
				}},
				{{
					Text:         lang.Button.Back,
					CallbackData: "open.menu",
				}},
			},
		},
		ParseMode: "MarkdownV2",
	}

	return page, nil
}
