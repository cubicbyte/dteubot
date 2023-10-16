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
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func handleStartCommand(u *tgbotapi.Update) error {
	cManager := utils.GetChatDataManager(u.FromChat().ID)
	uManager := utils.GetUserDataManager(u.SentFrom().ID)

	userData, err := uManager.GetUserData()
	if err != nil {
		return err
	}

	// Register referral if available
	if userData.Referral == "" && u.Message.CommandArguments() != "" {
		userData.Referral = u.Message.CommandArguments()
		if err := uManager.UpdateUserData(userData); err != nil {
			return err
		}
	}

	// Send greeting
	greeting, err := pages.CreateGreetingPage(cManager)
	if err != nil {
		return err
	}
	_, err = settings.Bot.Send(greeting.CreateMessage(cManager.ChatId))
	if err != nil {
		return err
	}

	// Send group selection
	structures, err := settings.Api.GetStructures()
	if err != nil {
		return err
	}
	var groupSelection *pages.Page
	if len(structures) == 1 {
		groupSelection, err = pages.CreateFacultiesListPage(cManager, structures[0].Id)
	} else {
		groupSelection, err = pages.CreateStructuresListPage(cManager)
	}
	if err != nil {
		return err
	}
	_, err = settings.Bot.Send(groupSelection.CreateMessage(cManager.ChatId))
	if err != nil {
		return err
	}

	return nil
}
