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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
)

func HandleSetClassesNotificationsButton(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, chat *data.Chat, chatRepo data.ChatRepository, user *data.User, groups *groupscache.Cache) error {
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	// Get button data
	state, ok := button.Params["state"]
	if !ok {
		return errors.New("notif param not found")
	}
	time2, ok := button.Params["time"]
	if !ok {
		return errors.New("time param not found")
	}
	_, isSuggestion := button.Params["suggestion"]

	// Update chat classes notifications settings
	switch time2 {
	case "15m":
		chat.ClassesNotification15m = state == "1"
	case "1m":
		chat.ClassesNotification1m = state == "1"
	default:
		return errors.New("invalid time in button data")
	}

	err := chatRepo.Update(chat)
	if err != nil {
		return err
	}

	// If it's a suggestion, send tooltip and close page
	if isSuggestion {
		// Send alert
		alertText := format.Formatm(lang.Alert.ClNotifEnabledTooltip, format.Values{
			"remaining": time2[0 : len(time2)-1],
		})
		alert := tgbotapi.NewCallbackWithAlert(u.CallbackQuery.ID, alertText)
		_, err = bot.Request(alert)
		if err != nil {
			return err
		}

		// Close page
		return ClosePage(u.CallbackQuery.Message.Chat.ID, u.CallbackQuery.Message.MessageID, bot, lang, user)
	}

	// Update page
	page, err := pages.CreateSettingsPage(lang, chat, chatRepo, groups)
	return editPage(page, err, u, bot)
}

func HandleSetClassesNotificationsNextPartButton(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, chat *data.Chat, chatRepo data.ChatRepository, groups *groupscache.Cache) error {
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	// Get state from button data
	state, ok := button.Params["state"]
	if !ok {
		return errors.New("state param not found")
	}

	// Update chat classes notifications settings
	chat.ClassesNotificationNextPart = state == "1"

	// Also set 15m notification to true if notifications is disabled
	if chat.ClassesNotificationNextPart && (!chat.ClassesNotification15m && !chat.ClassesNotification1m) {
		chat.ClassesNotification1m = true
	}

	err := chatRepo.Update(chat)
	if err != nil {
		return err
	}

	// Update page
	page, err := pages.CreateSettingsPage(lang, chat, chatRepo, groups)
	return editPage(page, err, u, bot)
}
