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
)

type ScheduleType string

const (
	ScheduleTypeGroup   ScheduleType = "group"
	ScheduleTypeStudent ScheduleType = "student"
	ScheduleTypeTeacher ScheduleType = "teacher"
)

func ParseScheduleType(s string) (ScheduleType, bool) {
	switch s {
	case string(ScheduleTypeGroup):
		return ScheduleTypeGroup, true
	case string(ScheduleTypeStudent):
		return ScheduleTypeStudent, true
	case string(ScheduleTypeTeacher):
		return ScheduleTypeTeacher, true
	default:
		return "", false
	}
}

func CreateScheduleTypeSelectionPage(lang i18n.Language) (Page, error) {
	page := Page{
		Text: lang.Page.ScheduleTypeSelection,
		ReplyMarkup: gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.Back,
					CallbackData: "open.menu#from=schedule_select",
				}}, {{
					Text:         lang.Button.ScheduleTypeGroup,
					CallbackData: "select.schedule_type#t=" + string(ScheduleTypeGroup),
				}}, {{
					Text:         lang.Button.ScheduleTypeStudent,
					CallbackData: "select.schedule_type#t=" + string(ScheduleTypeStudent),
				}}, {{
					Text:         lang.Button.ScheduleTypeTeacher,
					CallbackData: "select.schedule_type#t=" + string(ScheduleTypeTeacher),
				}},
			},
		},
		ParseMode:             "MarkdownV2",
		DisableWebPagePreview: true,
	}

	return page, nil
}
