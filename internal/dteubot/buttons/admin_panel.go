package buttons

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleAdminPanelButton(u *tgbotapi.Update) error {
	// Check if user is admin
	if adm, err := checkAdmin(u); err != nil || !adm {
		return err
	}

	cManager := utils.GetChatDataManager(u.FromChat().ID)

	page, err := pages.CreateAdminPanelPage(cManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}