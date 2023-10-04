package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/dteubot"
	logging_ "github.com/cubicbyte/dteubot/internal/logging"
	"github.com/op/go-logging"
	"os"
)

var log = logging.MustGetLogger("main")

func main() {
	err := config.LoadEnv()
	if err != nil {
		fmt.Printf("Error loading .env file: %s\n", err)
		pauseAndExit(1)
	}

	err = config.ValidateEnv()
	if err != nil {
		fmt.Printf("Error validating .env file: %s\n", err)
		pauseAndExit(1)
	}

	err = logging_.Init()
	if err != nil {
		fmt.Printf("Error initializing logging: %s\n", err)
		pauseAndExit(1)
	}

	dteubot.Setup()
	dteubot.Run()
}

func pauseAndExit(code int) {
	fmt.Println("Press Enter Key to continue...")
	if _, err := fmt.Scanln(); err != nil {
		return
	}
	os.Exit(code)
}
