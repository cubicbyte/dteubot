package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/i18n"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
	"time"
)

func CreateSchedulePage(cm *data.ChatDataManager, date time.Time) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	// TODO: Finish this

	page := Page{
		Text: getLocalizedDate(lang, date),
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}

func getLocalizedDate(lang *i18n.Language, date time.Time) string {
	// No better way to do this if it is not a map
	var month string
	switch date.Month() {
	case 1:
		month = lang.Text.ShortMonth1
	case 2:
		month = lang.Text.ShortMonth2
	case 3:
		month = lang.Text.ShortMonth3
	case 4:
		month = lang.Text.ShortMonth4
	case 5:
		month = lang.Text.ShortMonth5
	case 6:
		month = lang.Text.ShortMonth6
	case 7:
		month = lang.Text.ShortMonth7
	case 8:
		month = lang.Text.ShortMonth8
	case 9:
		month = lang.Text.ShortMonth9
	case 10:
		month = lang.Text.ShortMonth10
	case 11:
		month = lang.Text.ShortMonth11
	case 12:
		month = lang.Text.ShortMonth12
	}

	var weekday string
	switch date.Weekday() {
	case 1:
		weekday = lang.Text.WeekDay1
	case 2:
		weekday = lang.Text.WeekDay2
	case 3:
		weekday = lang.Text.WeekDay3
	case 4:
		weekday = lang.Text.WeekDay4
	case 5:
		weekday = lang.Text.WeekDay5
	case 6:
		weekday = lang.Text.WeekDay6
	case 7:
		weekday = lang.Text.WeekDay7
	}

	return format.Formatm(lang.Text.ScheduleDateFormat, format.Values{
		"day":     date.Day(),
		"month":   month,
		"year":    date.Year(),
		"weekday": weekday,
	})
}
