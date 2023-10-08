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

	if os.Getenv("API_URL") == "" {
		return &IncorrectEnvVariableError{"API_URL"}
	}

	// Optional env variables below
	if os.Getenv("API_REQUEST_TIMEOUT") != "" {
		_, err := strconv.ParseInt(os.Getenv("API_REQUEST_TIMEOUT"), 10, 64)
		if err != nil {
			return &IncorrectEnvVariableError{"API_REQUEST_TIMEOUT"}
		}
	}

	if os.Getenv("API_CACHE_EXPIRES") != "" {
		_, err := strconv.ParseInt(os.Getenv("API_CACHE_EXPIRES"), 10, 64)
		if err != nil {
			return &IncorrectEnvVariableError{"API_CACHE_EXPIRES"}
		}
	}

	if os.Getenv("NOTIFICATIONS_SUGGESTION_DELAY") != "" {
		_, err = strconv.ParseInt(os.Getenv("NOTIFICATIONS_SUGGESTION_DELAY"), 10, 64)
		if err != nil {
			return &IncorrectEnvVariableError{"NOTIFICATIONS_SUGGESTION_DELAY"}
		}
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
