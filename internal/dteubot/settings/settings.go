package settings

import (
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

var (
	Languages map[string]i18n.Language
	Bot       *tgbotapi.BotAPI
	Api       *api.Api
)
