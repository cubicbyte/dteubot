package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSetClassesNotificationsButton(u *tgbotapi.Update) error {
	// Get state & time from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	state, ok := button.Params["state"]
	if !ok {
		return errors.New("no state in button data")
	}
	time, ok := button.Params["time"]
	if !ok {
		return errors.New("no time in button data")
	}

	// Update chat classes notifications settings
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	chatData, err := cManager.GetChatData()
	if err != nil {
		return err
	}

	switch time {
	case "15m":
		chatData.ClassesNotification15m = state == "1"
	case "1m":
		chatData.ClassesNotification1m = state == "1"
	default:
		return errors.New("invalid time in button data")
	}

	err = cManager.UpdateChatData(chatData)
	if err != nil {
		return err
	}

	// Update page
	page, err := pages.CreateSettingsPage(&cManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
