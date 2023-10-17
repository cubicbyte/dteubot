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

package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSetClassesNotificationsButton(u *tgbotapi.Update) error {
	// Get state & time from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	state, ok := button.Params["state"]
	if !ok {
		return errors.New("no state in button data")
	}
	time, ok := button.Params["time"]
	if !ok {
		return errors.New("no time in button data")
	}

	// Update chat classes notifications settings
	cManager := utils.GetChatDataManager(u.FromChat().ID)

	chatData, err := cManager.GetChatData()
	if err != nil {
		return err
	}

	switch time {
	case "15m":
		chatData.ClassesNotification15m = state == "1"
	case "1m":
		chatData.ClassesNotification1m = state == "1"
	default:
		return errors.New("invalid time in button data")
	}

	err = cManager.UpdateChatData(chatData)
	if err != nil {
		return err
	}

	// Update page
	page, err := pages.CreateSettingsPage(cManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}

func HandleSetClassesNotificationsNextPartButton(u *tgbotapi.Update) error {
	// Get state & time from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	state, ok := button.Params["state"]
	if !ok {
		return errors.New("no state in button data")
	}

	// Update chat classes notifications settings
	cManager := utils.GetChatDataManager(u.FromChat().ID)

	chatData, err := cManager.GetChatData()
	if err != nil {
		return err
	}

	chatData.ClassesNotificationNextPart = state == "1"

	// Also set 15m notification to true if notifications is disabled
	if chatData.ClassesNotificationNextPart && (!chatData.ClassesNotification15m && !chatData.ClassesNotification1m) {
		chatData.ClassesNotification15m = true
	}

	err = cManager.UpdateChatData(chatData)
	if err != nil {
		return err
	}

	// Update page
	page, err := pages.CreateSettingsPage(cManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
