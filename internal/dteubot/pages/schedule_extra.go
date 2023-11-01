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
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
	"strconv"
	"strings"
	"unicode/utf8"
)

func CreateScheduleExtraInfoPage(lang *i18n.Language, groupId int, date string, api api.IApi) (*Page, error) {
	schedule, err := api.GetGroupScheduleDay(groupId, date)
	if err != nil {
		return nil, err
	}

	// Don't show multiple times the same extra text for the same lessons
	shownEntries := make(map[int]bool)

	pageExtraText := ""
	for _, lesson := range schedule.Lessons {
		for _, period := range lesson.Periods {
			if !period.ExtraText {
				continue
			}

			if _, ok := shownEntries[period.R1]; ok {
				continue
			} else {
				shownEntries[period.R1] = true
			}

			// Get extra info
			extraText, err := api.GetScheduleExtraInfo(period.R1, date)
			if err != nil {
				return nil, err
			}

			// Clean HTML from unsupported tags
			extraTextStr, err := utils.CleanHTML(extraText.Html)
			if err != nil {
				return nil, err
			}

			// Remove all spaces and newlines from the beginning and end of the string
			extraTextStr = strings.Trim(extraTextStr, "\n ")

			pageExtraText += "<b>" + strconv.Itoa(lesson.Number) + ")</b> " + extraTextStr + "\n\n"
		}
	}

	pageText := format.Formatp(lang.Page.ScheduleExtraInfo, pageExtraText)

	if utf8.RuneCountInString(pageText) > 4096 {
		// FIXME: This is vulnerable to HTML tags and can break the page.
		//   Create a function that will cut the string carefully, excluding HTML tags.
		//   This func should also support other formatting modes (Markdown, MarkdownV2, HTML)
		pageText = pageText[:4093] + "..."
	}

	page := Page{
		Text: pageText,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.schedule.day#date="+date),
			),
		),
		ParseMode:             "HTML",
		DisableWebPagePreview: true,
	}

	return &page, nil
}
