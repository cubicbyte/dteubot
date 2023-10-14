package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"github.com/sirkon/go-format/v2"
	"strconv"
	"strings"
	"time"
)

// List of teachers that are not found in the teachers list.
// Needed to prevent spamming the log with the same warnings.
var teacherPagesNotFound = make(map[string]bool)

var log = logging.MustGetLogger("Bot")

const ScheduleDateRange = 14

func CreateSchedulePage(cm *data.ChatDataManager, date string) (*Page, error) {
	date_, err := api.ParseISODate(date)
	if err != nil {
		return nil, err
	}

	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	lang, err := utils.GetChatLang(chatData)
	if err != nil {
		return nil, err
	}

	schedule, err := settings.Api.GetGroupScheduleDay(chatData.GroupId, date)
	if err != nil {
		return nil, err
	}

	var buttons tgbotapi.InlineKeyboardMarkup
	var pageText string

	if isNoLessons(schedule) {
		// Create empty schedule page
		skipLeft, skipRight, err := scanEmptyDays(chatData.GroupId, date_)
		if err != nil {
			return nil, err
		}

		if skipLeft == 0 {
			skipLeft = 1
		}
		if skipRight == 0 {
			skipRight = 1
		}

		nextDayDate := date_.AddDate(0, 0, skipRight)
		prevDayDate := date_.AddDate(0, 0, -skipLeft)
		nextWeekDate := date_.AddDate(0, 0, 7)
		prevWeekDate := date_.AddDate(0, 0, -7)

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
			pageText = format.Formatp(lang.Page.ScheduleEmptyDay, getLocalizedDate(lang, date_))
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
					"open.schedule.today",
				),
			)
		}
	} else {
		// Create schedule page
		pageText = getLocalizedDate(lang, date_) + "\n\n"

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
					"teachersNameFull":    getTeacher(period.TeachersNameFull),
				})
			}
		}

		prevDayDate := date_.AddDate(0, 0, -1)
		nextDayDate := date_.AddDate(0, 0, 1)
		prevWeekDate := date_.AddDate(0, 0, -7)
		nextWeekDate := date_.AddDate(0, 0, 7)

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
		if date != time.Now().In(settings.Location).Format("2006-01-02") {
			buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1] = append(
				buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1],
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.ScheduleNavigationToday,
					"open.schedule.today",
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
							"open.schedule.extra#date="+date,
						),
					),
				).InlineKeyboard,
				buttons.InlineKeyboard...,
			)
		}

		pageText += "`—————————————————————————`"
	}

	page := Page{
		Text:                  pageText,
		InlineKeyboard:        buttons,
		ParseMode:             "MarkdownV2",
		DisableWebPagePreview: true,
	}

	return &page, nil
}

// isNoLessons checks if there are no lessons in the given day
func isNoLessons(day *api.TimeTableDate) bool {
	for _, lesson := range day.Lessons {
		for _, period := range lesson.Periods {
			name := strings.ToLower(period.DisciplineShortName)
			if !strings.Contains(name, "приховано") {
				return false
			}
		}
	}

	return true
}

func getTeacher(teachersNameFull string) string {
	var teacher string

	// Get first teacher
	teachers := strings.Split(teachersNameFull, ", ")
	firstTeacher := teachers[0]
	teacher = firstTeacher

	// Escape markdown
	teacher = utils.EscapeTelegramMarkdownV2(teacher)

	// Get teacher profile link
	profileLink, ok := settings.TeachersList.GetLink(firstTeacher)
	if ok {
		teacher = "[" + teacher + "](" + profileLink + ")"
	} else {
		// Log warning if teacher page not found
		if _, ok := teacherPagesNotFound[firstTeacher]; !ok {
			log.Warningf("Teacher page not found: %s\n", firstTeacher)
			teacherPagesNotFound[firstTeacher] = true
		}
	}

	// If there is multiple teachers, return only the first one and add " +n" to the end
	if len(teachers) > 1 {
		teacher += " \\+" + strconv.Itoa(len(teachers)-1)
	}

	return teacher
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
			if isNoLessons(&day) {
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
