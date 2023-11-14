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
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/logging"
)

func HandleSendLogsButton(bot *gotgbot.Bot, ctx *ext.Context) error {
	// Check if user is admin
	user, err := userRepo.GetById(ctx.EffectiveUser.Id)
	if err != nil {
		return err
	}

	if !user.IsAdmin {
		return nil
	}

	// Send "sending document" action
	_, err = bot.SendChatAction(ctx.EffectiveChat.Id, "upload_document", nil)
	if err != nil {
		return err
	}

	// Send logs
	_, err = bot.SendDocument(ctx.EffectiveChat.Id, logging.LogFile, &gotgbot.SendDocumentOpts{
		Caption: "Logs",
	})
	if err != nil {
		return err
	}

	// Create "done" alert
	_, err = bot.AnswerCallbackQuery(ctx.CallbackQuery.Id, &gotgbot.AnswerCallbackQueryOpts{
		Text: "Done",
	})

	return nil
}
