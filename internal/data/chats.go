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
	_ "embed"
	"os"
	"time"
)

// Chat is a struct that contains all the chat settings
type Chat struct {
	Id                          int64     `db:"chat_id" json:"id"`
	GroupId                     int       `db:"group_id" json:"groupId"`
	LanguageCode                string    `db:"lang_code" json:"languageCode"`
	ClassesNotification15m      bool      `db:"cl_notif_15m" json:"clNotif15m"`
	ClassesNotification1m       bool      `db:"cl_notif_1m" json:"clNotif1m"`
	ClassesNotificationNextPart bool      `db:"cl_notif_next_part" json:"clNotifNextPart"`
	SeenSettings                bool      `db:"seen_settings" json:"seenSettings"`
	Accessible                  bool      `db:"accessible" json:"accessible"`
	Created                     time.Time `db:"created" json:"created"`
}

// ChatRepository is an interface for working with chat data.
type ChatRepository interface {
	// GetById returns a chat by its id.
	GetById(id int64) (*Chat, error)
	// Update updates a chat.
	Update(chat *Chat) error
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
