package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/dteubot"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	logging_ "github.com/cubicbyte/dteubot/internal/logging"
	"github.com/cubicbyte/dteubot/pkg/api"
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

	lang, ok := settings.Languages["uk"]
	if !ok {
		log.Error("Language 'uk' not found")
		pauseAndExit(1)
	}
	log.Infof("lang.Page.LeftNoMore: '%s'\n", lang.Page.LeftNoMore)

	myApi := api.Api{Url: "https://mia.mobil.knute.edu.ua"}
	calls, err := myApi.GetCallSchedule()
	if err != nil {
		log.Errorf("Error getting calls schedule: %s\n", err)
		pauseAndExit(1)
	}

	log.Infof("Loaded %d calls\n", len(calls))
	for _, call := range calls {
		log.Infof("%s - %s\n", call.TimeStart, call.TimeEnd)
	}

	pauseAndExit(0)
}

func pauseAndExit(code int) {
	fmt.Println("Press Enter Key to continue...")
	if _, err := fmt.Scanln(); err != nil {
		return
	}
	os.Exit(code)
}
