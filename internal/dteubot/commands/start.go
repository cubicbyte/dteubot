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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleStartCommand(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, user *data.User, userRepo data.UserRepository, api2 api.IApi) error {
	// Register referral if available
	if user.Referral == "" && u.Message.CommandArguments() != "" {
		user.Referral = u.Message.CommandArguments()
		if err := userRepo.Update(user); err != nil {
			return err
		}
	}

	// Send greeting
	greeting, err := pages.CreateGreetingPage(lang)
	if err != nil {
		return err
	}
	_, err = bot.Send(greeting.CreateSendMessageOpts(u.FromChat().ID))
	if err != nil {
		return err
	}

	// Send group selection page
	structures, err := api2.GetStructures()
	if err != nil {
		return err
	}

	var groupSelection *pages.Page
	if len(structures) == 1 {
		groupSelection, err = pages.CreateFacultiesListPage(lang, structures[0].Id, api2)
	} else {
		groupSelection, err = pages.CreateStructuresListPage(lang, api2)
	}

	if err != nil {
		return err
	}

	_, err = bot.Send(groupSelection.CreateSendMessageOpts(u.FromChat().ID))
	if err != nil {
		return err
	}

	return nil
}
