package buttons

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleClearCacheButton(u *tgbotapi.Update) error {
	// Check if user is admin
	if adm, err := checkAdmin(u); err != nil || !adm {
		return err
	}

	// TODO: Clear cache

	cManager := utils.GetChatDataManager(u.FromChat().ID)

	lang, err := utils.GetLang(cManager)
	if err != nil {
		return err
	}

	// Create "done" alert
	alert := tgbotapi.NewCallbackWithAlert(u.CallbackQuery.ID, lang.Alert.Done)

	_, err = settings.Bot.Request(alert)
	if err != nil {
		return err
	}

	return nil
}
