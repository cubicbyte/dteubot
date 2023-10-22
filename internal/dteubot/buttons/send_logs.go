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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/internal/logging"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSendLogsButton(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, user *data.User) error {
	if !user.IsAdmin {
		return nil
	}

	// Send "sending document" action
	action := tgbotapi.NewChatAction(u.CallbackQuery.Message.Chat.ID, tgbotapi.ChatUploadDocument)
	_, err := bot.Request(action)
	if err != nil {
		return err
	}

	// Send logs
	msg := tgbotapi.NewDocument(u.CallbackQuery.Message.Chat.ID, tgbotapi.FilePath(logging.LogFilePath))
	_, err = bot.Send(msg)
	if err != nil {
		return err
	}

	// Create "done" alert
	alert := tgbotapi.NewCallbackWithAlert(u.CallbackQuery.ID, lang.Alert.Done)
	_, err = bot.Request(alert)
	if err != nil {
		return err
	}

	return nil
}
