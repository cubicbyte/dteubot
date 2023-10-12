package settings

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api/cachedapi"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"time"
)

var (
	Bot          *tgbotapi.BotAPI
	Api          *cachedapi.CachedApi
	Db           *data.Database
	Languages    map[string]i18n.Language
	GroupsCache  *groupscache.Cache
	TeachersList *teachers.TeachersList
	Location     *time.Location
)
