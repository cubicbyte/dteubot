package commands

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func handleStartCommand(u *tgbotapi.Update) error {
	cManager := utils.GetChatDataManager(u.FromChat().ID)
	uManager := utils.GetUserDataManager(u.SentFrom().ID)

	userData, err := uManager.GetUserData()
	if err != nil {
		return err
	}

	// Register referral if available
	if userData.Referral == "" && u.Message.CommandArguments() != "" {
		userData.Referral = u.Message.CommandArguments()
		if err := uManager.UpdateUserData(userData); err != nil {
			return err
		}
	}

	// Send greeting
	greeting, err := pages.CreateGreetingPage(cManager)
	if err != nil {
		return err
	}
	_, err = settings.Bot.Send(greeting.CreateMessage(cManager.ChatId))
	if err != nil {
		return err
	}

	// Send group selection
	structures, err := settings.Api.GetStructures()
	if err != nil {
		return err
	}
	var groupSelection *pages.Page
	if len(structures) == 1 {
		groupSelection, err = pages.CreateFacultiesListPage(cManager, structures[0].Id)
	} else {
		groupSelection, err = pages.CreateStructuresListPage(cManager)
	}
	if err != nil {
		return err
	}
	_, err = settings.Bot.Send(groupSelection.CreateMessage(cManager.ChatId))
	if err != nil {
		return err
	}

	return nil
}
