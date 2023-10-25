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

// FileUserRepository implements UserRepository interface by storing data in files.
//
// Should be created via NewFileUserRepository.
type FileUserRepository struct {
	dir string
}

// NewFileUserRepository creates a new instance of FileUserRepository.
func NewFileUserRepository(dir string) (*FileUserRepository, error) {
	if err := os.MkdirAll(dir, 0755); err != nil {
		return nil, err
	}

	return &FileUserRepository{dir: dir}, nil
}

func (r *FileUserRepository) GetById(id int64) (*User, error) {
	user := new(User)

	file, err := os.Open(r.getUserFile(id))
	if errors.Is(err, os.ErrNotExist) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	defer file.Close()

	err = json.NewDecoder(file).Decode(user)
	if err != nil {
		return nil, err
	}

	return user, nil
}

func (r *FileUserRepository) Update(user *User) error {
	file, err := os.OpenFile(r.getUserFile(user.Id), os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		return err
	}

	defer file.Close()

	err = json.NewEncoder(file).Encode(user)
	if err != nil {
		return err
	}

	return nil
}

// getUserFile returns a path to the file with user data.
func (r *FileUserRepository) getUserFile(id int64) string {
	return r.dir + "/" + strconv.FormatInt(id, 10) + ".json"
}
