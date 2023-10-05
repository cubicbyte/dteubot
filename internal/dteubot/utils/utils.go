package utils

import (
	"github.com/cubicbyte/dteubot/internal/data"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"strings"
)

var log = logging.MustGetLogger("bot")

// Telegram markdownV2 characters to escape
var escapeCharsMarkdownV2 = []string{
	"_", "\\_",
	"*", "\\*",
	"[", "\\[",
	"]", "\\]",
	"(", "\\(",
	")", "\\)",
	"~", "\\~",
	"`", "\\`",
	">", "\\>",
	"#", "\\#",
	"+", "\\+",
	"-", "\\-",
	"=", "\\=",
	"|", "\\|",
	"{", "\\{",
	"}", "\\}",
	".", "\\.",
	"!", "\\!",
}

// InitDatabaseRecords initializes the database records
// for user and chat from given update.
func InitDatabaseRecords(upd *tgbotapi.Update) error {
	log.Debug("Initializing database records")

	// Check if the chat is in the database
	cm := data.ChatDataManager{ChatId: upd.FromChat().ID}

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
	um := data.UserDataManager{UserId: upd.SentFrom().ID}

	exists, err = um.IsUserExists()
	if err != nil {
		return err
	}
	if !exists {
		if _, err := um.CreateUserData(); err != nil {
			return err
		}
	}

	return nil
}

// GetSettingIcon returns the icon for the setting: ✅ or ❌
func GetSettingIcon(enabled bool) string {
	if enabled {
		return "✅"
	}
	return "❌"
}

// EscapeTelegramMarkdownV2 escapes the Telegram markdownV2 characters
func EscapeTelegramMarkdownV2(str string) string {
	replacer := strings.NewReplacer(escapeCharsMarkdownV2...)
	return replacer.Replace(str)
}
