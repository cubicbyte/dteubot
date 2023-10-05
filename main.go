package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/dteubot"
	logging_ "github.com/cubicbyte/dteubot/internal/logging"
	"os"
)

func main() {
	err := config.LoadEnv()
	if err != nil {
		fmt.Printf("Error loading .env file: %s\n", err)
		os.Exit(1)
	}

	err = config.ValidateEnv()
	if err != nil {
		fmt.Printf("Error validating .env file: %s\n", err)
		os.Exit(1)
	}

	err = logging_.Init()
	if err != nil {
		fmt.Printf("Error initializing logging: %s\n", err)
		os.Exit(1)
	}

	dteubot.Setup()
	dteubot.Run()
}
