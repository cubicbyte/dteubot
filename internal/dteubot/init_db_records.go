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

package dteubot

import (
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/data"
)

func InitDatabaseRecords(_ *gotgbot.Bot, ctx *ext.Context) error {
	log.Debug("Initializing database records")

	// Create chat if not exists
	if ctx.EffectiveChat != nil {
		chat, err := chatRepo.GetById(ctx.EffectiveChat.Id)
		if err != nil {
			return err
		}

		if chat == nil {
			log.Debug("Creating new chat record")

			chat = data.NewChat(ctx.EffectiveChat.Id)
			if err := chatRepo.Update(chat); err != nil {
				return err
			}
		}
	}

	// Create user if not exists
	if ctx.EffectiveUser != nil {
		user, err := userRepo.GetById(ctx.EffectiveUser.Id)
		if err != nil {
			return err
		}

		if user == nil {
			log.Debug("Creating new user record")

			user = data.NewUser(ctx.EffectiveUser.Id)
			if err := userRepo.Update(user); err != nil {
				return err
			}
		}
	}

	return nil
}
