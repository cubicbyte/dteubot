package buttons

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleMenuButton(u *tgbotapi.Update) error {
	cManager := utils.GetChatDataManager(u.FromChat().ID)
	uManager := utils.GetUserDataManager(u.SentFrom().ID)

	page, err := pages.CreateMenuPage(cManager, uManager)
	if err != nil {
		return err
	}

	_, err = settings.Bot.Send(EditMessageRequest(page, u.CallbackQuery))
	if err != nil {
		return err
	}

	return nil
}
