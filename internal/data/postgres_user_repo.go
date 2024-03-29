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
	//go:embed sql/get_user.sql
	getUserQuery string
	//go:embed sql/update_user.sql
	updateUserQuery string
)

// PostgresUserRepository implements UserRepository interface for PostgreSQL.
//
// Should be created via NewPostgresUserRepository.
type PostgresUserRepository struct {
	db *sqlx.DB
}

// NewPostgresUserRepository creates a new instance of PostgresUserRepository.
func NewPostgresUserRepository(db *sqlx.DB) UserRepository {
	return &PostgresUserRepository{db: db}
}

func (r *PostgresUserRepository) GetById(id int64) (*User, error) {
	user := &User{}
	err := r.db.Get(user, getUserQuery, id)

	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	return user, nil
}

func (r *PostgresUserRepository) Update(user *User) error {
	_, err := r.db.NamedExec(updateUserQuery, user)
	if err != nil {
		return err
	}

	return nil
}
