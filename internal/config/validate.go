// Package config contains functions for loading and validating environment variables
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

	if os.Getenv("API_URL") == "" {
		return &IncorrectEnvVariableError{"API_URL"}
	}

	_, err := strconv.ParseInt(os.Getenv("API_REQUEST_TIMEOUT"), 10, 64)
	if err != nil {
		return &IncorrectEnvVariableError{"API_REQUEST_TIMEOUT"}
	}

	_, err = strconv.ParseInt(os.Getenv("API_CACHE_EXPIRES"), 10, 64)
	if err != nil {
		return &IncorrectEnvVariableError{"API_CACHE_EXPIRES"}
	}

	_, err = strconv.ParseInt(os.Getenv("NOTIFICATIONS_SUGGESTION_DELAY"), 10, 64)
	if err != nil {
		return &IncorrectEnvVariableError{"NOTIFICATIONS_SUGGESTION_DELAY"}
	}

	switch os.Getenv("LOG_LEVEL") {
	case "DEBUG", "INFO", "WARNING", "ERROR", "DISABLED":
	default:
		return &IncorrectEnvVariableError{"LOG_LEVEL"}
	}

	logChatId := os.Getenv("LOG_CHAT_ID")
	if logChatId != "" {
		_, err = strconv.ParseInt(logChatId, 10, 64)
		if err != nil {
			return &IncorrectEnvVariableError{"LOG_CHAT_ID"}
		}
	}

	return nil
}
