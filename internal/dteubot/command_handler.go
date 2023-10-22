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
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/commands"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleCommand(u *tgbotapi.Update) error {
	command := u.Message.Command()

	if command == "" {
		// Not a command
		return nil
	}

	log.Infof("Handling command %s from %d\n", u.Message.Command(), u.Message.From.ID)

	chatRepo := data.NewPostgresChatRepository(db)
	userRepo := data.NewPostgresUserRepository(db)

	chat, err := chatRepo.GetById(u.FromChat().ID)
	if err != nil {
		return err
	}
	if chat == nil {
		return errors.New("chat not found")
	}

	user, err := userRepo.GetById(u.FromChat().ID)
	if err != nil {
		return err
	}
	if user == nil {
		return errors.New("user not found")
	}

	lang, err := utils.GetLang(chat.LanguageCode, languages)
	if err != nil {
		return err
	}

	switch u.Message.Command() {
	case "start":
		return commands.HandleStartCommand(u, bot, lang, user, userRepo, api)
	case "today", "t":
		return commands.HandleTodayCommand(u, bot, lang, chat, api, teachersList)
	case "tomorrow", "tt":
		return commands.HandleTomorrowCommand(u, bot, lang, chat, api, teachersList)
	case "left", "l":
		return commands.HandleLeftCommand(u, bot, lang, chat, api)
	case "calls", "c":
		return commands.HandleCallsCommand(u, bot, lang, api)
	case "settings":
		return commands.HandleSettingsCommand(u, bot, lang, chat, chatRepo, groupsCache)
	case "lang", "language":
		return commands.HandleLanguageCommand(u, bot, lang, languages)
	case "group", "g", "select":
		return commands.HandleGroupCommand(u, bot, lang, chat, chatRepo, groupsCache, api)
	default:
		// Not our command
		return nil
	}
}
