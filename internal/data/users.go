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
	"time"
)

// User is a struct that contains all the user data
type User struct {
	Id        int64     `db:"id" json:"id"`
	FirstName string    `db:"first_name" json:"firstName"`
	LastName  string    `db:"last_name" json:"lastName"`
	Username  string    `db:"username" json:"username"`
	IsAdmin   bool      `db:"is_admin" json:"isAdmin"`
	Referral  string    `db:"referral" json:"referral"`
	Created   time.Time `db:"created" json:"created"`
}

// UserRepository is an interface for working with user data.
type UserRepository interface {
	// GetById returns a user by its id.
	GetById(id int64) (*User, error)
	// Update updates the user data.
	Update(user *User) error
}

// NewUser creates a new instance of User.
func NewUser(id int64) *User {
	return &User{
		Id:        id,
		FirstName: "",
		LastName:  "",
		Username:  "",
		IsAdmin:   false,
		Referral:  "",
		Created:   time.Now(),
	}
}
