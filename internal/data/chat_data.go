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

package data

import (
	"github.com/patrickmn/go-cache"
	"os"
	"strconv"
	"time"
)

// ChatDataManager makes it easier to work with chat data.
type ChatDataManager struct {
	ChatId   int64
	Database *Database
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
	err := m.Database.Db.Get(chatData, GetChatQuery, m.ChatId)
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

	_, err := m.Database.Db.NamedExec(UpdateChatQuery, chatData)
	if err != nil {
		return err
	}

	return nil
}

// CreateChatData creates chat data record in database for the chat.
func (m *ChatDataManager) CreateChatData() (*ChatData, error) {
	log.Debugf("Creating chat data for chat %d\n", m.ChatId)

	chatData := new(ChatData)
	err := m.Database.Db.Get(chatData, CreateChatQuery, m.ChatId, os.Getenv("DEFAULT_LANG"))
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
	err := m.Database.Db.Get(&exists, IsChatExistsQuery, m.ChatId)
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
