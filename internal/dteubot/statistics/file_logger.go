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

package statistics

import (
	"os"
	"strconv"
	"time"
)

const ButtonClicksDirPath = "buttons"
const CommandsDirPath = "commands"

// FileLogger is a logger that logs statistics events to the files.
//
// It implements Logger interface.
type FileLogger struct {
	dir string
}

// NewFileLogger creates a new logger that logs statistics events to the files.
func NewFileLogger(dir string) (Logger, error) {
	// Create directories if they don't exist
	if err := os.MkdirAll(dir, 0755); err != nil {
		return nil, err
	}
	if err := os.MkdirAll(dir+"/"+ButtonClicksDirPath, 0755); err != nil {
		return nil, err
	}
	if err := os.MkdirAll(dir+"/"+CommandsDirPath, 0755); err != nil {
		return nil, err
	}

	return &FileLogger{dir: dir}, nil
}

func (l *FileLogger) LogButtonClick(chatId int64, userId int64, messageId int, button string) error {
	// Open file to append, create if it doesn't exist
	file, err := os.OpenFile(l.getButtonFilePath(chatId), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	defer file.Close()

	// Write string to file
	str := time.Now().In(time.UTC).Format("2006-01-02 15:04:05.000") +
		" " + strconv.FormatInt(chatId, 10) +
		" " + strconv.FormatInt(userId, 10) +
		" " + strconv.Itoa(messageId) + " " + button

	if _, err := file.WriteString(str + "\n"); err != nil {
		return err
	}

	return nil
}

func (l *FileLogger) LogCommand(chatId int64, userId int64, messageId int, command string) error {
	// Open file to append, create if it doesn't exist
	file, err := os.OpenFile(l.getCommandFilePath(chatId), os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}

	// Write string to file
	str := time.Now().In(time.UTC).Format("2006-01-02 15:04:05.000") +
		" " + strconv.FormatInt(chatId, 10) +
		" " + strconv.FormatInt(userId, 10) +
		" " + strconv.Itoa(messageId) + " " + command

	if _, err := file.WriteString(str + "\n"); err != nil {
		return err
	}

	return nil
}

func (l *FileLogger) getCommandFilePath(chatId int64) string {
	return l.dir + "/" + CommandsDirPath + "/" + strconv.FormatInt(chatId, 10) + ".txt"
}

func (l *FileLogger) getButtonFilePath(chatId int64) string {
	return l.dir + "/" + ButtonClicksDirPath + "/" + strconv.FormatInt(chatId, 10) + ".txt"
}
