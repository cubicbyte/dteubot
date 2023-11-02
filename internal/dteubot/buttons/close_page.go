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
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/i18n"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strings"
)

func HandleClosePageButton(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, user *data.User) error {
	return ClosePage(u.CallbackQuery.Message.Chat.ID, u.CallbackQuery.Message.MessageID, bot, lang, user)
}

// ClosePage closes page or changes it to menu page
func ClosePage(chatId int64, messageId int, bot *tgbotapi.BotAPI, lang *i18n.Language, user *data.User) error {
	_, err := bot.Request(tgbotapi.NewDeleteMessage(chatId, messageId))

	if err != nil {
		// Check if error is because of message is older than 48 hours
		var tgError *tgbotapi.Error
		if errors.As(err, &tgError) && tgError.Code == 400 {
			if strings.HasPrefix(tgError.Message, "Bad Request: message can't be deleted for everyone") {
				// Edit message to menu page
				page, err := pages.CreateMenuPage(lang, user)
				if err != nil {
					return err
				}

				_, err = bot.Send(page.CreateEditMessage(chatId, messageId))
				if err != nil {
					return err
				}

				return nil
			}
		}

		return err
	}

	return nil
}