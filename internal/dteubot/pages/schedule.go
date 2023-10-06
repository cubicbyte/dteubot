package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
	"strconv"
	"time"
)

const ScheduleDateRange = 14

func CreateSchedulePage(cm *data.ChatDataManager, date time.Time) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	schedule, err := settings.Api.GetGroupScheduleDay(chatData.GroupId, date.Format("2006-01-02"))
	if err != nil {
		return nil, err
	}

	var buttons tgbotapi.InlineKeyboardMarkup
	var pageText string

	if len(schedule.Lessons) == 0 {
		// Create empty schedule page
		skipLeft, skipRight, err := scanEmptyDays(chatData.GroupId, date)
		if err != nil {
			return nil, err
		}

		if skipLeft == 0 {
			skipLeft = 1
		}
		if skipRight == 0 {
			skipRight = 1
		}

		nextDayDate := date.AddDate(0, 0, skipRight)
		prevDayDate := date.AddDate(0, 0, -skipLeft)
		nextWeekDate := date.AddDate(0, 0, 7)
		prevWeekDate := date.AddDate(0, 0, -7)

		now := time.Now().In(settings.Location)
		enableTodayButton := !(nextDayDate.After(now) && now.After(prevDayDate))

		if skipLeft > 1 || skipRight > 1 {
			// Create multiple days empty schedule page
			pageText = format.Formatm(lang.Page.ScheduleMultipleEmptyDays, format.Values{
				"dateStart": getLocalizedDate(lang, prevDayDate.AddDate(0, 0, 1)),
				"dateEnd":   getLocalizedDate(lang, nextDayDate.AddDate(0, 0, -1)),
			})
		} else {
			// Create single day empty schedule page
			pageText = format.Formatp(lang.Page.ScheduleEmptyDay, getLocalizedDate(lang, date))
		}

		buttons = tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationPreviousDay,
					"open.schedule.day#date="+prevDayDate.Format("2006-01-02"),
				),
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationNextDay,
					"open.schedule.day#date="+nextDayDate.Format("2006-01-02"),
				),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationPreviousWeek,
					"open.schedule.day#date="+prevWeekDate.Format("2006-01-02"),
				),
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationNextWeek,
					"open.schedule.day#date="+nextWeekDate.Format("2006-01-02"),
				),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Menu, "open.menu"),
			),
		)

		if enableTodayButton {
			buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1] = append(
				buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1],
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationToday,
					"open.schedule.day#date="+now.Format("2006-01-02"),
				),
			)
		}
	} else {
		// Create schedule page
		pageText = getLocalizedDate(lang, date) + "\n\n"

		for _, lesson := range schedule.Lessons {
			for _, period := range lesson.Periods {
				format_ := "`———— ``$timeStart`` ——— ``$timeEnd`` ————`\n`  `*$disciplineShortName*`[$typeStr]`\n`$lessonNumber `$classroom\n`  `$teachersNameFull\n"
				lessonNumber := strconv.Itoa(lesson.Number)
				pageText += format.Formatm(format_, format.Values{
					"timeStart":           utils.EscapeTelegramMarkdownV2(period.TimeStart),
					"timeEnd":             utils.EscapeTelegramMarkdownV2(period.TimeEnd),
					"disciplineShortName": utils.EscapeTelegramMarkdownV2(period.DisciplineShortName),
					"typeStr":             utils.EscapeTelegramMarkdownV2(period.TypeStr),
					"lessonNumber":        utils.EscapeTelegramMarkdownV2(lessonNumber),
					"classroom":           utils.EscapeTelegramMarkdownV2(period.Classroom),
					"teachersNameFull":    utils.EscapeTelegramMarkdownV2(period.TeachersNameFull),
				})
			}
		}

		prevDayDate := date.AddDate(0, 0, -1)
		nextDayDate := date.AddDate(0, 0, 1)
		prevWeekDate := date.AddDate(0, 0, -7)
		nextWeekDate := date.AddDate(0, 0, 7)

		buttons = tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationPreviousDay,
					"open.schedule.day#date="+prevDayDate.Format("2006-01-02"),
				),
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationNextDay,
					"open.schedule.day#date="+nextDayDate.Format("2006-01-02"),
				),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationPreviousWeek,
					"open.schedule.day#date="+prevWeekDate.Format("2006-01-02"),
				),
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationNextWeek,
					"open.schedule.day#date="+nextWeekDate.Format("2006-01-02"),
				),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Menu, "open.menu"),
			),
		)

		// Add today button if needed
		today := time.Now().In(settings.Location).Format("2006-01-02")
		if date.Format("2006-01-02") != today {
			buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1] = append(
				buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1],
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationToday,
					"open.schedule.day#date="+today,
				),
			)
		}

		// Add extra info button if needed
		if checkExtraText(schedule) {
			// Add to the start
			buttons.InlineKeyboard = append(
				tgbotapi.NewInlineKeyboardMarkup(
					tgbotapi.NewInlineKeyboardRow(
						tgbotapi.NewInlineKeyboardButtonData(
							lang.Button.ScheduleExtra,
							"open.schedule.extra#date="+date.Format("2006-01-02"),
						),
					),
				).InlineKeyboard,
				buttons.InlineKeyboard...,
			)
		}

		pageText += "`—————————————————————————`"
	}

	page := Page{
		Text:           pageText,
		InlineKeyboard: buttons,
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}

func checkExtraText(day *api.TimeTableDate) bool {
	for _, lesson := range day.Lessons {
		for _, period := range lesson.Periods {
			if period.ExtraText {
				return true
			}
		}
	}
	return false
}

func scanEmptyDays(groupId int, date time.Time) (int, int, error) {
	dateStart, dateEnd := api.GetDateRange(date, ScheduleDateRange)

	schedule, err := settings.Api.GetGroupSchedule(
		groupId,
		dateStart.Format("2006-01-02"),
		dateEnd.Format("2006-01-02"),
	)

	skipLeft, err := countNoLessonsDays(&schedule, date, false)
	if err != nil {
		return 0, 0, err
	}

	skipRight, err := countNoLessonsDays(&schedule, date, true)
	if err != nil {
		return 0, 0, err
	}

	return skipLeft, skipRight, nil
}

func countNoLessonsDays(days *[]api.TimeTableDate, date time.Time, directionRight bool) (int, error) {
	count := 0

	if directionRight {
		for _, day := range *days {
			date_, err := api.ParseISODate(day.Date)
			if err != nil {
				return 0, err
			}
			if date_.Before(date) {
				continue
			}
			if len(day.Lessons) == 0 {
				count++
			} else {
				break
			}
		}
	} else {
		for i := len(*days) - 1; i >= 0; i-- {
			date_, err := api.ParseISODate((*days)[i].Date)
			if err != nil {
				return 0, err
			}
			if date_.After(date) {
				continue
			}
			day := (*days)[i]
			if len(day.Lessons) == 0 {
				count++
			} else {
				break
			}
		}
	}

	return count, nil
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
