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

package commands

import (
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"strings"
)

func HandleStartCommand(bot *gotgbot.Bot, ctx *ext.Context) error {
	// Get chat and user
	chat, err := chatRepo.GetById(ctx.EffectiveChat.Id)
	if err != nil {
		return err
	}

	user, err := userRepo.GetById(ctx.EffectiveUser.Id)
	if err != nil {
		return err
	}

	lang, err := utils.GetLang(chat.LanguageCode, languages)
	if err != nil {
		return err
	}

	// Register referral if available
	if user.Referral == "" && strings.Contains(ctx.EffectiveMessage.Text, " ") {
		user.Referral = strings.SplitN(ctx.EffectiveMessage.Text, " ", 2)[1]
		if err := userRepo.Update(user); err != nil {
			return err
		}
	}

	// Send greeting
	greeting, err := pages.CreateGreetingPage(lang)
	if err != nil {
		return err
	}

	opts := greeting.CreateSendMessageOpts()
	_, err = bot.SendMessage(ctx.EffectiveChat.Id, greeting.Text, &opts)
	if err != nil {
		return err
	}

	// Send group selection page
	structures, err := api.GetStructures()
	if err != nil {
		return err
	}

	var groupSelection pages.Page
	if len(structures) == 1 {
		groupSelection, err = pages.CreateFacultiesListPage(lang, structures[0].Id)
	} else {
		groupSelection, err = pages.CreateStructuresListPage(lang)
	}

	if err != nil {
		return err
	}

	opts = groupSelection.CreateSendMessageOpts()
	_, err = bot.SendMessage(ctx.EffectiveChat.Id, groupSelection.Text, &opts)
	if err != nil {
		return err
	}

	return nil
}
