package settings

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"time"
)

var (
	Bot          *tgbotapi.BotAPI
	Api          *api.Api
	Languages    map[string]i18n.Language
	TeachersList *teachers.TeachersList
	Location     *time.Location
)
