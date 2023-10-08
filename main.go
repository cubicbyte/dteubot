package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/dteubot"
	logging_ "github.com/cubicbyte/dteubot/internal/logging"
	"os"
)

func main() {
	// Load .env file
	if err := config.LoadEnv(); err != nil {
		fmt.Printf("Error loading .env file: %s\n", err)
		os.Exit(1)
	}

	// Validate environment variables (config)
	if err := config.ValidateEnv(); err != nil {
		fmt.Printf("Error validating .env file: %s\n", err)
		os.Exit(1)
	}

	// Initialize logging
	if err := logging_.Init(); err != nil {
		fmt.Printf("Error initializing logging: %s\n", err)
		os.Exit(1)
	}

	dteubot.Setup()
	dteubot.Run()
}
