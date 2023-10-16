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
	"math/rand"
	"strconv"
	"time"
)

func CreateLeftPage(cm *data.ChatDataManager, backButton string) (*Page, error) {

	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	lang, err := utils.GetChatLang(chatData)
	if err != nil {
		return nil, err
	}

	// Get time left
	status, err := utils.GetCallsStatus(chatData.GroupId, time.Now().In(settings.Location))
	if err != nil {
		return nil, err
	}

	var pageText string
	if status == nil {
		pageText = format.Formatp(lang.Page.LeftUnknown, utils.DaysScanLimit)
	} else {
		timeLeft := status.Time.Sub(time.Now().In(settings.Location))
		timeLeftStr := utils.FormatDuration(timeLeft, 2, lang)

		switch status.Status {
		case utils.CallStatusBeforeStart:
			pageText = format.Formatp(lang.Page.LeftToClassesStart, timeLeftStr)
		case utils.CallStatusBefore:
			pageText = format.Formatp(lang.Page.LeftToLessonStart, timeLeftStr)
		case utils.CallStatusDuring:
			pageText = format.Formatp(lang.Page.LeftToLessonEnd, timeLeftStr)
		}
	}

	rand_ := strconv.Itoa(rand.Intn(1e6))
	page := Page{
		Text: pageText,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backButton),
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Refresh, "open.left#refresh&rnd="+rand_),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
