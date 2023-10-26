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
	"fmt"
	"os"
	"strconv"
)

// IncorrectEnvVariableError is an error that is returned when
// an environment variable has an incorrect value
type IncorrectEnvVariableError struct {
	EnvVariable string
}

func (e *IncorrectEnvVariableError) Error() string {
	return fmt.Sprintf("Incorrect env variable: %s. Please check .env file", e.EnvVariable)
}

// ValidateEnv validates all environment variables needed for the bot to work
func ValidateEnv() error {
	if os.Getenv("BOT_TOKEN") == "" {
		return &IncorrectEnvVariableError{"BOT_TOKEN"}
	}

	switch os.Getenv("DATABASE_TYPE") {
	case "postgres":
		if os.Getenv("POSTGRES_HOST") == "" {
			return &IncorrectEnvVariableError{"POSTGRES_HOST"}
		}

		_, err := strconv.ParseInt(os.Getenv("POSTGRES_PORT"), 10, 64)
		if err != nil {
			return &IncorrectEnvVariableError{"POSTGRES_PORT"}
		}

		if os.Getenv("POSTGRES_USER") == "" {
			return &IncorrectEnvVariableError{"POSTGRES_USER"}
		}

		if os.Getenv("POSTGRES_PASSWORD") == "" {
			return &IncorrectEnvVariableError{"POSTGRES_PASSWORD"}
		}

		if os.Getenv("POSTGRES_DB") == "" {
			return &IncorrectEnvVariableError{"POSTGRES_DB"}
		}

		switch os.Getenv("POSTGRES_SSL") {
		case "true", "false":
		default:
			return &IncorrectEnvVariableError{"POSTGRES_SSL"}
		}

	case "file":
		// Do nothing

	case "":
		if err := os.Setenv("DATABASE_TYPE", "file"); err != nil {
			return err
		}

	default:
		return &IncorrectEnvVariableError{"DATABASE_TYPE"}
	}

	if os.Getenv("API_URL") == "" {
		return &IncorrectEnvVariableError{"API_URL"}
	}

	// Optional env variables below

	if os.Getenv("API_REQUEST_TIMEOUT") == "" {
		if err := os.Setenv("API_REQUEST_TIMEOUT", "1000"); err != nil {
			return err
		}
	}
	_, err := strconv.ParseInt(os.Getenv("API_REQUEST_TIMEOUT"), 10, 64)
	if err != nil {
		return &IncorrectEnvVariableError{"API_REQUEST_TIMEOUT"}
	}

	if os.Getenv("API_CACHE_EXPIRES") == "" {
		if err := os.Setenv("API_CACHE_EXPIRES", "3600"); err != nil {
			return err
		}
	}
	_, err = strconv.ParseInt(os.Getenv("API_CACHE_EXPIRES"), 10, 64)
	if err != nil {
		return &IncorrectEnvVariableError{"API_CACHE_EXPIRES"}
	}

	if os.Getenv("NOTIFICATIONS_SUGGESTION_DELAY") == "" {
		if err := os.Setenv("NOTIFICATIONS_SUGGESTION_DELAY", "60"); err != nil {
			return err
		}
	}
	_, err = strconv.ParseInt(os.Getenv("NOTIFICATIONS_SUGGESTION_DELAY"), 10, 64)
	if err != nil {
		return &IncorrectEnvVariableError{"NOTIFICATIONS_SUGGESTION_DELAY"}
	}

	if os.Getenv("LOG_CHAT_ID") != "" {
		_, err = strconv.ParseInt(os.Getenv("LOG_CHAT_ID"), 10, 64)
		if err != nil {
			return &IncorrectEnvVariableError{"LOG_CHAT_ID"}
		}
	}

	switch os.Getenv("LOG_LEVEL") {
	case "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "DISABLED", "":
	default:
		return &IncorrectEnvVariableError{"LOG_LEVEL"}
	}

	return nil
}
