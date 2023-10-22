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
	"database/sql"
	_ "embed"
	"errors"
	"github.com/jmoiron/sqlx"
	"os"
	"time"
)

// Load SQL queries from files
var (
	//go:embed sql/get_chat.sql
	getChatQuery string
	//go:embed sql/update_chat.sql
	updateChatQuery string
)

// Chat is a struct that contains all the chat settings
type Chat struct {
	Id                          int64     `db:"chat_id"`
	GroupId                     int       `db:"group_id"`
	LanguageCode                string    `db:"lang_code"`
	ClassesNotification15m      bool      `db:"cl_notif_15m"`
	ClassesNotification1m       bool      `db:"cl_notif_1m"`
	ClassesNotificationNextPart bool      `db:"cl_notif_next_part"`
	SeenSettings                bool      `db:"seen_settings"`
	Accessible                  bool      `db:"accessible"`
	Created                     time.Time `db:"created"`
}

// ChatRepository is an interface for working with chat data.
type ChatRepository interface {
	GetById(id int64) (*Chat, error)
	Update(chat *Chat) error
}

// PostgresChatRepository implements ChatRepository interface for PostgreSQL.
//
// Should be created via NewPostgresChatRepository.
type PostgresChatRepository struct {
	db *sqlx.DB
}

// NewPostgresChatRepository creates a new instance of PostgresChatRepository.
func NewPostgresChatRepository(db *sqlx.DB) *PostgresChatRepository {
	return &PostgresChatRepository{db: db}
}

// GetById returns a chat by its id.
func (r *PostgresChatRepository) GetById(id int64) (*Chat, error) {
	chat := new(Chat)
	err := r.db.Get(chat, getChatQuery, id)

	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	return chat, nil
}

// Update updates a chat.
func (r *PostgresChatRepository) Update(chat *Chat) error {
	_, err := r.db.NamedExec(updateChatQuery, chat)
	if err != nil {
		return err
	}

	return nil
}

// NewChat creates a new instance of Chat.
func NewChat(id int64) *Chat {
	return &Chat{
		Id:                          id,
		GroupId:                     -1,
		LanguageCode:                os.Getenv("DEFAULT_LANG"),
		ClassesNotification15m:      false,
		ClassesNotification1m:       false,
		ClassesNotificationNextPart: false,
		SeenSettings:                false,
		Accessible:                  true,
		Created:                     time.Now(),
	}
}
