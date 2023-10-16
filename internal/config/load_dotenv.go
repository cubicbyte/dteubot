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

package config

import (
	_ "embed"
	"github.com/joho/godotenv"
	"os"
)

// Embed .env.example file and create .env file if it doesn't exist
//
//go:embed .env.example
var envExample []byte

// LoadEnv loads environment variables from .env file
// and creates it if it doesn't exist
func LoadEnv() error {
	// Create .env file if it doesn't exist
	if _, err := os.Stat(".env"); os.IsNotExist(err) {
		err := os.WriteFile(".env", envExample, 0644)
		if err != nil {
			return err
		}
	}

	// Load .env file
	err := godotenv.Load(".env")
	if err != nil {
		return err
	}

	return nil
}
