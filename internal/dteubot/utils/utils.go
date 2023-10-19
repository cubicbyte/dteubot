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

package utils

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/i18n"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"os"
	"strings"
	"time"
)

var log = logging.MustGetLogger("bot")

// InitDatabaseRecords initializes the database records
// for user and chat from given update.
func InitDatabaseRecords(upd *tgbotapi.Update) error {
	log.Debug("Initializing database records")

	// Check if the chat is in the database
	cm := GetChatDataManager(upd.FromChat().ID)

	exists, err := cm.IsChatExists()
	if err != nil {
		return err
	}
	if !exists {
		if _, err := cm.CreateChatData(); err != nil {
			return err
		}
	}

	if upd.SentFrom() == nil {
		return nil
	}

	// Check if the user is in the database
	um := GetUserDataManager(upd.SentFrom().ID)

	exists, err = um.IsUserExists()
	if err != nil {
		return err
	}
	if !exists {
		userData, err := um.CreateUserData()
		if err != nil {
			return err
		}

		// Update user data
		userData.FirstName = upd.SentFrom().FirstName
		userData.LastName = upd.SentFrom().LastName
		userData.Username = upd.SentFrom().UserName
		userData.LanguageCode = upd.SentFrom().LanguageCode
		err = um.UpdateUserData(userData)
		if err != nil {
			return err
		}
	}

	// Update user data
	userData, err := um.GetUserData()
	if err != nil {
		return err
	}

	if userData.FirstName != upd.SentFrom().FirstName ||
		userData.LastName != upd.SentFrom().LastName ||
		userData.Username != upd.SentFrom().UserName ||
		userData.LanguageCode != upd.SentFrom().LanguageCode ||
		userData.IsPremium != upd.SentFrom().IsPremium {

		// Update found
		userData.FirstName = upd.SentFrom().FirstName
		userData.LastName = upd.SentFrom().LastName
		userData.Username = upd.SentFrom().UserName
		userData.LanguageCode = upd.SentFrom().LanguageCode
		userData.IsPremium = upd.SentFrom().IsPremium

		err = um.UpdateUserData(userData)
		if err != nil {
			return err
		}
	}

	return nil
}

// EscapeText takes an input text and escape Telegram markup symbols.
// In this way we can send a text without being afraid of having to escape the characters manually.
// Note that you don't have to include the formatting style in the input text, or it will be escaped too.
// If there is an error, an empty string will be returned.
//
// parseMode is the text formatting mode (ModeMarkdown, ModeMarkdownV2 or ModeHTML)
// text is the input string that will be escaped
//
// TODO: Remove this when merged: https://github.com/go-telegram-bot-api/telegram-bot-api/pull/604
func EscapeText(parseMode string, text string) string {
	var replacer *strings.Replacer

	if parseMode == tgbotapi.ModeHTML {
		replacer = strings.NewReplacer("<", "&lt;", ">", "&gt;", "&", "&amp;")
	} else if parseMode == tgbotapi.ModeMarkdown {
		replacer = strings.NewReplacer("_", "\\_", "*", "\\*", "`", "\\`", "[", "\\[")
	} else if parseMode == tgbotapi.ModeMarkdownV2 {
		replacer = strings.NewReplacer(
			"\\", "\\\\",
			"_", "\\_", "*", "\\*", "[", "\\[", "]", "\\]", "(",
			"\\(", ")", "\\)", "~", "\\~", "`", "\\`", ">", "\\>",
			"#", "\\#", "+", "\\+", "-", "\\-", "=", "\\=", "|",
			"\\|", "{", "\\{", "}", "\\}", ".", "\\.", "!", "\\!",
		)
	} else {
		return ""
	}

	return replacer.Replace(text)
}

// GetSettingIcon returns the icon for the setting: ✅ or ❌
func GetSettingIcon(enabled bool) string {
	if enabled {
		return "✅"
	}
	return "❌"
}

// ParseTime parses time in given layout with local timezone
func ParseTime(layout string, value string) (time.Time, error) {
	return time.ParseInLocation(layout, value, settings.Location)
}

// GetChatDataManager returns ChatDataManager for given chat ID.
func GetChatDataManager(chatId int64) *data.ChatDataManager {
	return &data.ChatDataManager{ChatId: chatId, Database: settings.Db}
}

// GetUserDataManager returns UserDataManager for given user ID.
func GetUserDataManager(userId int64) *data.UserDataManager {
	return &data.UserDataManager{UserId: userId, Database: settings.Db}
}

// GetLang returns the language of the chat.
func GetLang(cm *data.ChatDataManager) (*i18n.Language, error) {
	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	return GetChatLang(chatData)
}

// GetChatLang returns the language of the chat from given ChatData.
func GetChatLang(chatData *data.ChatData) (*i18n.Language, error) {
	// Use default language if chat language is not set
	var langCode string
	if chatData.LanguageCode == "" {
		langCode = os.Getenv("DEFAULT_LANG")
	} else {
		langCode = chatData.LanguageCode
	}

	// Get language
	lang, ok := settings.Languages[langCode]
	if !ok {
		return nil, &i18n.LanguageNotFoundError{LangCode: langCode}
	}

	return &lang, nil
}
