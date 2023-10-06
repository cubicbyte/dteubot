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
	// No better way to do this if lang is a struct
	var month string
	switch date.Month() {
	case time.January:
		month = lang.Text.ShortMonth1
	case time.February:
		month = lang.Text.ShortMonth2
	case time.March:
		month = lang.Text.ShortMonth3
	case time.April:
		month = lang.Text.ShortMonth4
	case time.May:
		month = lang.Text.ShortMonth5
	case time.June:
		month = lang.Text.ShortMonth6
	case time.July:
		month = lang.Text.ShortMonth7
	case time.August:
		month = lang.Text.ShortMonth8
	case time.September:
		month = lang.Text.ShortMonth9
	case time.October:
		month = lang.Text.ShortMonth10
	case time.November:
		month = lang.Text.ShortMonth11
	case time.December:
		month = lang.Text.ShortMonth12
	}

	var weekday string
	switch date.Weekday() {
	case time.Monday:
		weekday = lang.Text.WeekDay1
	case time.Tuesday:
		weekday = lang.Text.WeekDay2
	case time.Wednesday:
		weekday = lang.Text.WeekDay3
	case time.Thursday:
		weekday = lang.Text.WeekDay4
	case time.Friday:
		weekday = lang.Text.WeekDay5
	case time.Saturday:
		weekday = lang.Text.WeekDay6
	case time.Sunday:
		weekday = lang.Text.WeekDay7
	}

	return format.Formatm(lang.Text.ScheduleDateFormat, format.Values{
		"day":     date.Day(),
		"month":   month,
		"year":    date.Year(),
		"weekday": weekday,
	})
}
