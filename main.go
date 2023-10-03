package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/i18n"
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

	langs, err := i18n.LoadLangs()
	if err != nil {
		fmt.Printf("Error loading languages: %s\n", err)
		pause()
	}

	log.Infof("Loaded %d languages\n", len(langs))
	lang, ok := langs["uk"]
	if !ok {
		log.Error("Language 'uk' not found")
		pause()
		os.Exit(1)
	}
	log.Infof("lang.Page.LeftNoMore: '%s'\n", lang.Page.LeftNoMore)

	pause()
	os.Exit(0)
}

func pause() {
	fmt.Println("Press Enter Key to continue...")
	fmt.Scanln()
}
