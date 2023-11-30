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

package errorhandler

import (
	"fmt"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"runtime/debug"
)

// PanicsHandler handles panics in the code and sends them to the user.
//
// Implements the ext.DispatcherPanicHandler interface.
func PanicsHandler(b *gotgbot.Bot, ctx *ext.Context, r interface{}) {
	log.Errorf("Panic: %s\n%s", r, string(debug.Stack()))

	if ctx.EffectiveChat == nil {
		// Send error to the developer
		SendErrorToTelegram(fmt.Errorf("panic: %s\n%s", r, string(debug.Stack())), b)
		return
	}

	// Send error page to chat
	chat, err := chatRepo.GetById(ctx.EffectiveChat.Id)
	if err != nil {
		log.Errorf("Error getting chat: %s\n", err)
		SendErrorToTelegram(err, b)
		return
	}

	lang, err := utils.GetLang(chat.LanguageCode, langs)
	if err != nil {
		log.Errorf("Error getting language: %s\n", err)
		SendErrorToTelegram(err, b)
		return
	}

	SendErrorPageToChat(ctx, b, lang)
	SendErrorToTelegram(fmt.Errorf("panic: %s\n%s", r, string(debug.Stack())), b)
}
