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
