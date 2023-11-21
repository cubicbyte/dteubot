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
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/dlclark/regexp2"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"os"
	"strings"
	"time"
)

var log = logging.MustGetLogger("bot")

// InitDatabaseRecords initializes the database records
// for user and chat from given update.
func InitDatabaseRecords(upd *tgbotapi.Update, chatRepo data.ChatRepository, userRepo data.UserRepository) error {
	log.Debug("Initializing database records")

	fromChat := upd.FromChat()
	sentFrom := upd.SentFrom()

	// Check if the chat is in the database
	chat, err := chatRepo.GetById(fromChat.ID)
	if err != nil {
		return err
	}

	if chat == nil {
		// Chat not found, create a new one
		chat = data.NewChat(fromChat.ID)
		err := chatRepo.Update(chat)
		if err != nil {
			return err
		}
	}

	// Check if the user is in the database
	if sentFrom == nil {
		return nil
	}
	user, err := userRepo.GetById(sentFrom.ID)
	if err != nil {
		return err
	}

	if user == nil {
		// User not found, create a new one
		user = data.NewUser(sentFrom.ID)

		// Update user data
		user.FirstName = sentFrom.FirstName
		user.LastName = sentFrom.LastName
		user.Username = sentFrom.UserName
		user.LanguageCode = sentFrom.LanguageCode
		user.IsPremium = sentFrom.IsPremium

		err = userRepo.Update(user)
		if err != nil {
			return err
		}

		return nil
	}

	// Check if user data has changed
	if user.FirstName != sentFrom.FirstName ||
		user.LastName != sentFrom.LastName ||
		user.Username != sentFrom.UserName ||
		user.LanguageCode != sentFrom.LanguageCode ||
		user.IsPremium != sentFrom.IsPremium {

		// Update found
		user.FirstName = sentFrom.FirstName
		user.LastName = sentFrom.LastName
		user.Username = sentFrom.UserName
		user.LanguageCode = sentFrom.LanguageCode
		user.IsPremium = sentFrom.IsPremium

		err = userRepo.Update(user)
		if err != nil {
			return err
		}
	}

	return nil
}

// CleanHTML removes all unsupported HTML tags from given text.
func CleanHTML(text string) string {
	telegramSupportedHTMLTags := [...]string{
		"a", "s", "i", "b", "u", "em", "pre",
		"ins", "del", "code", "strong", "strike",
	}

	// Save line breaks
	// <br> <br/> <br /> <p>
	text = strings.ReplaceAll(text, "<p>", "\n")
	text = strings.ReplaceAll(text, "<br>", "\n")
	text = strings.ReplaceAll(text, "<br/>", "\n")
	text = strings.ReplaceAll(text, "<br />", "\n")

	// Remove all other tags
	// tag|tag2|tag3
	supported := strings.Join(telegramSupportedHTMLTags[:], "|")
	cleanr := regexp2.MustCompile("<(?!\\/?("+supported+")\\b)[^>]*>", regexp2.IgnoreCase)
	text, _ = cleanr.Replace(text, "", -1, -1)

	return text
}

// CleanText removes unnecessary characters from given text:
//   - Too many newlines
//   - Spaces and newlines from the beginning and end of the string
func CleanText(text string) string {
	// Remove newlines like this: \n \n
	re := regexp2.MustCompile(`\n[^\S\r\n]+`, regexp2.IgnoreCase)
	text, _ = re.Replace(text, "\n", -1, -1)

	// Remove too many newlines
	re = regexp2.MustCompile(`\n{3,}`, regexp2.IgnoreCase)
	text, _ = re.Replace(text, "\n\n", -1, -1)

	// Remove all spaces and newlines from the beginning and end of the string
	text = strings.Trim(text, "\n ")

	return text
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

// GetLang returns the language of the chat.
func GetLang(code string, langs map[string]i18n.Language) (*i18n.Language, error) {
	if code == "" {
		code = os.Getenv("DEFAULT_LANG")
	}

	lang, ok := langs[code]
	if !ok {
		return nil, &i18n.LanguageNotFoundError{LangCode: code}
	}

	return &lang, nil
}

// SetLocation sets the location of the time without changing the time itself.
func SetLocation(time2 time.Time, location *time.Location) time.Time {
	return time.Date(time2.Year(), time2.Month(), time2.Day(), time2.Hour(), time2.Minute(), time2.Second(), time2.Nanosecond(), location)
}

// SplitRows splits the given slice into rows of given size.
//
// slice is the slice to split
// rowSize is the size of each row
//
// Example:
//
//	slice := []int{1, 2, 3, 4, 5, 6, 7, 8}
//	rows := SplitRows(slice, 3)
//	// rows = [[1, 2, 3], [4, 5, 6], [7, 8]]
func SplitRows[T any](slice []T, rowSize int) [][]T {
	rowsCount := len(slice) / rowSize
	if len(slice)%rowSize != 0 {
		rowsCount++
	}
	rows := make([][]T, rowsCount)

	lastRow := make([]T, min(rowSize, len(slice)))
	for i, item := range slice {
		lastRow[i%rowSize] = item
		if i%rowSize == rowSize-1 {
			rows[i/rowSize] = lastRow
			lastRow = make([]T, min(rowSize, len(slice)-i-1))
		}
	}
	if len(lastRow) > 0 {
		rows[len(rows)-1] = lastRow
	}

	return rows
}

// GetLessonIcon returns the icon for the lesson type.
//
// Examples (*colored emoji):
//   - Lecture:  🔸
//   - Practice: 🔹
//   - Exam:     🔺
func GetLessonIcon(lessonType int) string {
	/*
		Лк - 1
		Пз* - 2
		Лб* - 4
		Екз - 5
		Зач - 6
		КонсЕкз - 20
	*/
	switch lessonType {
	case 1:
		return "🔸"
	case 2, 4:
		return "🔹"
	case 5, 6, 20:
		return "🔺"
	default:
		return ""
	}
}
