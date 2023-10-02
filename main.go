package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"os"
)

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
}

func pause() {
	fmt.Println("Press Enter Key to exit...")
	fmt.Scanln()
	os.Exit(1)
}
