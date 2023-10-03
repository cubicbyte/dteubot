package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	logging_ "github.com/cubicbyte/dteubot/internal/logging"
	"github.com/op/go-logging"
	"os"
)

var log = logging.MustGetLogger("main")

func main() {
	err := config.LoadEnv()
	if err != nil {
		fmt.Printf("Error loading .env file: %s\n", err)
		pause()
	}

	err = config.ValidateEnv()
	if err != nil {
		fmt.Printf("Error validating .env file: %s\n", err)
		pause()
	}

	err = logging_.Init()
	if err != nil {
		fmt.Printf("Error initializing logging: %s\n", err)
		pause()
	}

	log.Error("Test error! Press Enter Key to exit")
	fmt.Scanln()
}

func pause() {
	fmt.Println("Press Enter Key to exit...")
	fmt.Scanln()
	os.Exit(1)
}
