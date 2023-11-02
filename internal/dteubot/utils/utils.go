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
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/dlclark/regexp2"
	"github.com/go-telegram/bot/models"
	"os"
	"strings"
	"time"
)

// CleanHTML removes all unsupported HTML tags from given text.
func CleanHTML(text string) (string, error) {
	telegramSupportedHTMLTags := [...]string{
		"a", "s", "i", "b", "u", "em", "pre",
		"ins", "del", "code", "strong", "strike",
	}

	// Save line breaks
	text = strings.ReplaceAll(text, "<br>", "\n")
	text = strings.ReplaceAll(text, "<br/>", "\n")
	text = strings.ReplaceAll(text, "<br />", "\n")

	// Remove all other tags
	// tag|tag2|tag3
	supported := strings.Join(telegramSupportedHTMLTags[:], "|")
	cleanr, err := regexp2.Compile("<(?!\\/?("+supported+")\\b)[^>]*>", regexp2.IgnoreCase)
	if err != nil {
		return "", err
	}

	text, err = cleanr.Replace(text, "", -1, -1)
	if err != nil {
		return "", err
	}

	return text, nil
}

// EscapeMarkdownV2 takes an input text and escape Telegram MarkdownV2 markup symbols.
//
// TODO: Remove this when merged: https://github.com/go-telegram/bot/pull/44
func EscapeMarkdownV2(text string) string {
	replacer := strings.NewReplacer(
		"\\", "\\\\",
		"_", "\\_", "*", "\\*", "[", "\\[", "]", "\\]", "(",
		"\\(", ")", "\\)", "~", "\\~", "`", "\\`", ">", "\\>",
		"#", "\\#", "+", "\\+", "-", "\\-", "=", "\\=", "|",
		"\\|", "{", "\\{", "}", "\\}", ".", "\\.", "!", "\\!",
	)

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

// GetUpdChat returns the chat from the given update.
func GetUpdChat(u *models.Update) *models.Chat {
	if u.Message != nil {
		return &u.Message.Chat
	} else if u.CallbackQuery != nil {
		return &u.CallbackQuery.Message.Chat
	} else if u.EditedMessage != nil {
		return &u.EditedMessage.Chat
	} else if u.ChannelPost != nil {
		return &u.ChannelPost.Chat
	} else if u.EditedChannelPost != nil {
		return &u.EditedChannelPost.Chat
	} else if u.MyChatMember != nil {
		return &u.MyChatMember.Chat
	} else if u.ChatMember != nil {
		return &u.ChatMember.Chat
	}

	return nil
}

// GetUpdUser returns the user from the given update.
func GetUpdUser(u *models.Update) *models.User {
	if u.Message != nil {
		return u.Message.From
	} else if u.CallbackQuery != nil {
		return &u.CallbackQuery.Sender
	} else if u.EditedMessage != nil {
		return u.EditedMessage.From
	} else if u.ChannelPost != nil {
		return u.ChannelPost.From
	} else if u.EditedChannelPost != nil {
		return u.EditedChannelPost.From
	} else if u.MyChatMember != nil {
		return &u.MyChatMember.From
	} else if u.ChatMember != nil {
		return &u.ChatMember.From
	}

	return nil
}

// GetUpdMessage returns the message from the given update.
func GetUpdMessage(u *models.Update) *models.Message {
	if u.Message != nil {
		return u.Message
	} else if u.CallbackQuery != nil {
		return u.CallbackQuery.Message
	} else if u.EditedMessage != nil {
		return u.EditedMessage
	} else if u.ChannelPost != nil {
		return u.ChannelPost
	} else if u.EditedChannelPost != nil {
		return u.EditedChannelPost
	}

	return nil
}

// GetMsgCommand returns the command from the given message. If there is no command, returns an empty string.
//
// Example: /start@bot -> start
func GetMsgCommand(msg *models.Message) string {
	if msg == nil {
		return ""
	}

	if !IsCommand(msg) {
		return ""
	}

	entity := msg.Entities[0]
	command := msg.Text[1:entity.Length]

	// Remove bot username from command: /start@bot -> /start
	if i := strings.Index(command, "@"); i != -1 {
		command = command[:i]
	}

	return command
}

// IsCommand returns true if the given message is a bot command.
func IsCommand(m *models.Message) bool {
	if m.Entities == nil || len(m.Entities) == 0 {
		return false
	}

	entity := m.Entities[0]
	return entity.Offset == 0 && entity.Type == "bot_command"
}
