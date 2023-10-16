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
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("bot")

func HandleCommand(update tgbotapi.Update) (bool, error) {
	cmd := update.Message.Command()

	// If there is no command, return
	if cmd == "" {
		return false, nil
	}

	log.Infof("Handling message %s\n", update.Message.Text)

	switch cmd {
	case "start":
		if err := handleStartCommand(&update); err != nil {
			return false, err
		}
	case "today", "t":
		if err := handleTodayCommand(&update); err != nil {
			return false, err
		}
	case "tomorrow":
		if err := handleTomorrowCommand(&update); err != nil {
			return false, err
		}
	case "left", "l":
		if err := handleLeftCommand(&update); err != nil {
			return false, err
		}
	case "calls", "c":
		if err := handleCallsCommand(&update); err != nil {
			return false, err
		}
	case "settings":
		if err := handleSettingsCommand(&update); err != nil {
			return false, err
		}
	case "lang", "language":
		if err := handleLanguageCommand(&update); err != nil {
			return false, err
		}
	case "group", "g", "select":
		if err := handleGroupCommand(&update); err != nil {
			return false, err
		}
	default:
		// Not our command
		return false, nil
	}

	return true, nil
}
