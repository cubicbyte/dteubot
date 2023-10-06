package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSelectLanguageButton(u *tgbotapi.Update) error {
	// Get language from button data
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	lang, ok := button.Params["lang"]
	if !ok {
		return errors.New("no lang in button data")
	}

	// Update chat language
	cManager := data.ChatDataManager{ChatId: u.CallbackQuery.Message.Chat.ID}

	chatData, err := cManager.GetChatData()
	if err != nil {
		return err
	}

	// If language is already set, go to settings page
	if chatData.LanguageCode == lang {
		page, err := pages.CreateSettingsPage(&cManager)
		if err != nil {
			return err
		}

		_, err = settings.Bot.Send(editMessageReq(page, u.CallbackQuery))
		if err != nil {
			return err
		}

		return nil
	}

	chatData.LanguageCode = lang
	err = cManager.UpdateChatData(chatData)
	if err != nil {
		return err
	}

	// Update page
	page, err := pages.CreateLanguageSelectionPage(&cManager, "open.settings#from=lang")
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(editMessageReq(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
