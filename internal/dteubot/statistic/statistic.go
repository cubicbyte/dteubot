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

package statistic

import (
	_ "embed"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/op/go-logging"
)

var (
	//go:embed sql/log_button_click.sql
	logButtonClickQuery string
	//go:embed sql/log_command.sql
	logCommandQuery string
)

var log = logging.MustGetLogger("Statistic")

// LogButtonClick logs a button click to the database for statistic purposes.
func LogButtonClick(chatId int64, userId int64, messageId int, button string) error {
	log.Debug("Logging button click")

	// Truncate button to 64 characters
	if len(button) > 64 {
		button = button[:64]
	}

	_, err := settings.Db.Db.Exec(logButtonClickQuery, chatId, userId, messageId, button)
	return err
}

// LogCommand logs a bot command to the database for statistic purposes.
func LogCommand(chatId int64, userId int64, messageId int, command string) error {
	log.Debug("Logging command")

	// Truncate command to 64 characters
	if len(command) > 64 {
		command = command[:64]
	}

	_, err := settings.Db.Db.Exec(logCommandQuery, chatId, userId, messageId, command)
	return err
}
