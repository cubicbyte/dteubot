package dteubot

import (
	"github.com/cubicbyte/dteubot/internal/db"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"os"
	"time"
)

// ChatDataManager makes it easier to work with chat data.
type ChatDataManager struct {
	ChatId int64
}

// ChatData is a struct that contains all the data about a chat.
type ChatData struct {
	ChatId                 int64     `db:"chat_id"`
	GroupId                int       `db:"group_id"`
	LanguageCode           string    `db:"lang_code"`
	ClassesNotification15m bool      `db:"cl_notif_15m"`
	ClassesNotification1m  bool      `db:"cl_notif_1m"`
	SeenSettings           bool      `db:"seen_settings"`
	Accessible             bool      `db:"accessible"`
	Created                time.Time `db:"created"`
}

// GetChatData returns chat data for the chat.
func (m *ChatDataManager) GetChatData() (*ChatData, error) {
	log.Debugf("Getting chat data for chat %d\n", m.ChatId)

	chatData := new(ChatData)
	err := Database.Db.Get(chatData, db.GetChatQuery, m.ChatId)
	if err != nil {
		return nil, err
	}

	return chatData, nil
}

// UpdateChatData updates chat data for the chat.
func (m *ChatDataManager) UpdateChatData(chatData *ChatData) error {
	log.Debugf("Updating chat data for chat %d\n", chatData.ChatId)

	_, err := Database.Db.NamedExec(db.UpdateChatQuery, chatData)
	if err != nil {
		return err
	}

	return nil
}

// CreateChatData creates chat data record in database for the chat.
func (m *ChatDataManager) CreateChatData() error {
	log.Debugf("Creating chat data for chat %d\n", m.ChatId)

	_, err := Database.Db.Exec(db.CreateChatQuery, m.ChatId, os.Getenv("DEFAULT_LANG"))
	if err != nil {
		return err
	}

	return nil
}

// IsChatExists checks if the chat exists in the database.
func (m *ChatDataManager) IsChatExists() (bool, error) {
	log.Debugf("Checking if chat %d exists\n", m.ChatId)

	var exists bool
	err := Database.Db.Get(&exists, db.IsChatExistsQuery, m.ChatId)
	if err != nil {
		return false, err
	}

	return exists, nil
}

// GetLanguage returns the language of the chat.
func (m *ChatDataManager) GetLanguage() (*i18n.Language, error) {
	// Get chat data
	chatData, err := m.GetChatData()
	if err != nil {
		return nil, err
	}

	// Use default language if chat language is not set
	var langCode string
	if chatData.LanguageCode == "" {
		langCode = os.Getenv("DEFAULT_LANG")
	} else {
		langCode = chatData.LanguageCode
	}

	// Get language
	lang, ok := Languages[langCode]
	if !ok {
		return nil, &i18n.LanguageNotFoundError{LangCode: langCode}
	}

	return &lang, nil
}
