package main

import (
	"errors"
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/i18n"
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

	myApi := api.Api{"https://mia.mobil.knute.edu.ua"}
	calls, err := myApi.GetCallSchedule()
	if err != nil {
		log.Errorf("Error getting calls schedule: %s\n", err)
		if errors.Is(err, &api.ApiError{}) {
			log.Errorf("HTTP status code: %d\n", err.(*api.ApiError).Code)
		}
		pause()
		os.Exit(1)
	}

	log.Infof("Loaded %d calls\n", len(calls))
	for _, call := range calls {
		log.Infof("%s - %s\n", call.TimeStart, call.TimeEnd)
	}

	pause()
	os.Exit(0)
}

func pause() {
	fmt.Println("Press Enter Key to continue...")
	fmt.Scanln()
}
