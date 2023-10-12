package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func HandleSelectGroupButton(u *tgbotapi.Update) error {
	// Get group id from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)
	groupId, ok := button.Params["groupId"]
	if !ok {
		return errors.New("no groupId in button data")
	}
	groupId_, err := strconv.Atoi(groupId)
	if err != nil {
		return err
	}

	// Update chat group id
	uManager := data.UserDataManager{UserId: u.CallbackQuery.From.ID}
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	chatData, err := cManager.GetChatData()
	if err != nil {
		return err
	}

	chatData.GroupId = groupId_
	err = cManager.UpdateChatData(chatData)
	if err != nil {
		return err
	}

	// Create page
	page, err := pages.CreateMenuPage(&cManager, &uManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
