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
)

// Load SQL queries from files
var (
	//go:embed sql/get_chat.sql
	getChatQuery string
	//go:embed sql/update_chat.sql
	updateChatQuery string

	//go:embed sql/get_chats_15m.sql
	getChats15mQuery string
	//go:embed sql/get_chats_1m.sql
	getChats1mQuery string
)

// PostgresChatRepository implements ChatRepository interface for PostgreSQL.
//
// Should be created via NewPostgresChatRepository.
type PostgresChatRepository struct {
	db *sqlx.DB
}

// NewPostgresChatRepository creates a new instance of PostgresChatRepository.
func NewPostgresChatRepository(db *sqlx.DB) ChatRepository {
	return &PostgresChatRepository{db: db}
}

// TODO: Optimize pointer usage, like here: r *PostgresChatRepository -> r PostgresChatRepository

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

func (r *PostgresChatRepository) Update(chat *Chat) error {
	_, err := r.db.NamedExec(updateChatQuery, chat)
	if err != nil {
		return err
	}

	return nil
}

func (r *PostgresChatRepository) GetChatsWithEnabled15mNotification() ([]*Chat, error) {
	chats := make([]*Chat, 0)
	err := r.db.Select(&chats, getChats15mQuery)

	if err != nil {
		return nil, err
	}

	return chats, nil
}

func (r *PostgresChatRepository) GetChatsWithEnabled1mNotification() ([]*Chat, error) {
	chats := make([]*Chat, 0)
	err := r.db.Select(&chats, getChats1mQuery)

	if err != nil {
		return nil, err
	}

	return chats, nil
}
