package data

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/patrickmn/go-cache"
	"os"
	"strconv"
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

	// Get from cache
	cachedData, ok := chatCache.Get(strconv.FormatInt(m.ChatId, 10))
	if ok {
		return cachedData.(*ChatData), nil
	}

	// Get from database
	chatData := new(ChatData)
	err := DbInstance.Db.Get(chatData, GetChatQuery, m.ChatId)
	if err != nil {
		return nil, err
	}

	// Add to cache
	err = chatCache.Add(strconv.FormatInt(m.ChatId, 10), chatData, cache.DefaultExpiration)
	if err != nil {
		return nil, err
	}

	return chatData, nil
}

// UpdateChatData updates chat data for the chat.
func (m *ChatDataManager) UpdateChatData(chatData *ChatData) error {
	log.Debugf("Updating chat data for chat %d\n", chatData.ChatId)

	_, err := DbInstance.Db.NamedExec(UpdateChatQuery, chatData)
	if err != nil {
		return err
	}

	return nil
}

// CreateChatData creates chat data record in database for the chat.
func (m *ChatDataManager) CreateChatData() (*ChatData, error) {
	log.Debugf("Creating chat data for chat %d\n", m.ChatId)

	chatData := new(ChatData)
	err := DbInstance.Db.Get(chatData, CreateChatQuery, m.ChatId, os.Getenv("DEFAULT_LANG"))
	if err != nil {
		return nil, err
	}

	return chatData, nil
}

// IsChatExists checks if the chat exists in the database.
func (m *ChatDataManager) IsChatExists() (bool, error) {
	log.Debugf("Checking if chat %d exists\n", m.ChatId)

	// Check from cache
	_, ok := chatCache.Get(strconv.FormatInt(m.ChatId, 10))
	if ok {
		return true, nil
	}

	// Check from database
	var exists bool
	err := DbInstance.Db.Get(&exists, IsChatExistsQuery, m.ChatId)
	if err != nil {
		return false, err
	}

	return exists, nil
}

// GetOrCreateChatData returns chat data for the chat or creates it if it doesn't exist.
func (m *ChatDataManager) GetOrCreateChatData() (*ChatData, error) {
	// Check if chat data exists
	exists, err := m.IsChatExists()
	if err != nil {
		return nil, err
	}

	// Create chat data if it doesn't exist
	if !exists {
		chatData, err := m.CreateChatData()
		if err != nil {
			return nil, err
		}
		return chatData, nil
	}

	// Get chat data
	chatData, err := m.GetChatData()
	if err != nil {
		return nil, err
	}

	return chatData, nil
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
	lang, ok := settings.Languages[langCode]
	if !ok {
		return nil, &i18n.LanguageNotFoundError{LangCode: langCode}
	}

	return &lang, nil
}
