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
	"encoding/json"
	"errors"
	"os"
	"strconv"
)

// FileChatRepository implements ChatRepository interface using file system.
//
// Should be created via NewFileChatRepository.
type FileChatRepository struct {
	dir string
}

// NewFileChatRepository creates a new instance of FileChatRepository.
func NewFileChatRepository(dir string) (*FileChatRepository, error) {
	if err := os.MkdirAll(dir, 0755); err != nil {
		return nil, err
	}

	return &FileChatRepository{dir: dir}, nil
}

func (r *FileChatRepository) GetById(id int64) (*Chat, error) {
	chat := new(Chat)

	file, err := os.Open(r.getChatFile(id))
	if errors.Is(err, os.ErrNotExist) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	defer file.Close()

	err = json.NewDecoder(file).Decode(chat)
	if err != nil {
		return nil, err
	}

	return chat, nil
}

func (r *FileChatRepository) Update(chat *Chat) error {
	file, err := os.OpenFile(r.getChatFile(chat.Id), os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		return err
	}

	defer file.Close()

	err = json.NewEncoder(file).Encode(chat)
	if err != nil {
		return err
	}

	return nil
}

// getChatFile returns a path to a file with chat data.
func (r *FileChatRepository) getChatFile(id int64) string {
	return r.dir + "/" + strconv.FormatInt(id, 10) + ".json"
}
