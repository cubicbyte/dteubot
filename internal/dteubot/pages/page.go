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

package pages

import (
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/i18n"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
)

var (
	chatRepo     data.ChatRepository
	userRepo     data.UserRepository
	api          api2.Api
	groupsCache  *groupscache.Cache
	teachersList *teachers.TeachersList
	languages    map[string]i18n.Language
)

// InitPages initializes the pages package. Must be called before using the package
func InitPages(
	chatRepo2 data.ChatRepository,
	userRepo2 data.UserRepository,
	api2 api2.Api,
	groupsCache2 *groupscache.Cache,
	teachersList2 *teachers.TeachersList,
	languages2 map[string]i18n.Language,
) {
	chatRepo = chatRepo2
	userRepo = userRepo2
	api = api2
	groupsCache = groupsCache2
	teachersList = teachersList2
	languages = languages2
}

// Page represents a telegram page
type Page struct {
	Text                  string
	ReplyMarkup           gotgbot.InlineKeyboardMarkup
	ParseMode             string
	DisableWebPagePreview bool
}

// CreateSendMessageOpts creates a telegram message parameters from the page
func (p Page) CreateSendMessageOpts() gotgbot.SendMessageOpts {
	return gotgbot.SendMessageOpts{
		ParseMode:             p.ParseMode,
		DisableWebPagePreview: p.DisableWebPagePreview,
		ReplyMarkup:           p.ReplyMarkup,
	}
}

// CreateEditMessageOpts creates a telegram edit message parameters from the page
func (p Page) CreateEditMessageOpts(chatId int64, messageId int64) gotgbot.EditMessageTextOpts {
	return gotgbot.EditMessageTextOpts{
		ChatId:                chatId,
		MessageId:             messageId,
		ParseMode:             p.ParseMode,
		DisableWebPagePreview: p.DisableWebPagePreview,
		ReplyMarkup:           p.ReplyMarkup,
	}
}
