/*
 * Copyright (c) 2022 Bohdan Marukhnenko
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package pages

import (
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/cubicbyte/dteubot/internal/dteubot/teachers"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
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

func CreateSchedulePage(lang i18n.Language, groupId int, date string) (Page, error) {
	date_, err := api2.ParseISODate(date)
	if err != nil {
		return Page{}, err
	}

	day, err := api.GetGroupScheduleDay(groupId, date)
	if err != nil {
		return Page{}, err
	}

	var buttons gotgbot.InlineKeyboardMarkup
	var pageText string

	if isNoLessons(day) {
		// Get more days if there are no lessons
		dateStart, dateEnd := api2.GetDateRange(date_, ScheduleDateRange)
		schedule, err := api.GetGroupSchedule(
			groupId,
			dateStart.Format("2006-01-02"),
			dateEnd.Format("2006-01-02"),
		)

		// Create empty schedule page
		skipLeft, skipRight, err := ScanEmptyDays(schedule, date_)
		if err != nil {
			return Page{}, err
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

		now := time.Now()
		today := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, now.Location())
		enableTodayButton := !(nextDayDate.After(today) && today.After(prevDayDate))

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

		buttons = gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.ScheduleNavigationPreviousDay,
					CallbackData: "open.schedule.day#date=" + prevDayDate.Format("2006-01-02"),
				}, {
					Text:         lang.Button.ScheduleNavigationNextDay,
					CallbackData: "open.schedule.day#date=" + nextDayDate.Format("2006-01-02"),
				}},
				{{
					Text:         lang.Button.ScheduleNavigationPreviousWeek,
					CallbackData: "open.schedule.day#date=" + prevWeekDate.Format("2006-01-02"),
				}, {
					Text:         lang.Button.ScheduleNavigationNextWeek,
					CallbackData: "open.schedule.day#date=" + nextWeekDate.Format("2006-01-02"),
				}},
				{{
					Text:         lang.Button.Menu,
					CallbackData: "open.menu",
				}},
			},
		}

		if enableTodayButton {
			buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1] = append(
				buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1],
				gotgbot.InlineKeyboardButton{
					Text:         lang.Button.ScheduleNavigationToday,
					CallbackData: "open.schedule.today",
				},
			)
		}
	} else {
		// Create schedule page
		pageText = getLocalizedDate(lang, date_) + "\n\n"

		for _, lesson := range day.Lessons {
			for _, period := range lesson.Periods {
				format_ := "`———— ``$timeStart`` ——— ``$timeEnd`` ————`\n`  `$lessonIcon *$disciplineShortName*`[$typeStr]`\n`$lessonNumber `$classroom\n`  `$teachersNameFull\n"
				lessonNumber := strconv.Itoa(lesson.Number)
				lessonIcon := utils.GetLessonIcon(period.Type)

				pageText += format.Formatm(format_, format.Values{
					"timeStart":           utils.EscapeMarkdownV2(period.TimeStart),
					"timeEnd":             utils.EscapeMarkdownV2(period.TimeEnd),
					"disciplineShortName": utils.EscapeMarkdownV2(period.DisciplineShortName),
					"typeStr":             utils.EscapeMarkdownV2(period.TypeStr),
					"lessonNumber":        utils.EscapeMarkdownV2(lessonNumber),
					"classroom":           utils.EscapeMarkdownV2(period.Classroom),
					"teachersNameFull":    getTeacher(period.TeachersNameFull, teachersList),
					"lessonIcon":          lessonIcon,
				})

				if lessonIcon == "" {
					log.Warningf("Could not get lesson icon for lesson type %d (%s)\n", period.Type, period.TypeStr)
				}
			}
		}

		prevDayDate := date_.AddDate(0, 0, -1)
		nextDayDate := date_.AddDate(0, 0, 1)
		prevWeekDate := date_.AddDate(0, 0, -7)
		nextWeekDate := date_.AddDate(0, 0, 7)

		buttons = gotgbot.InlineKeyboardMarkup{
			InlineKeyboard: [][]gotgbot.InlineKeyboardButton{
				{{
					Text:         lang.Button.ScheduleNavigationPreviousDay,
					CallbackData: "open.schedule.day#date=" + prevDayDate.Format("2006-01-02"),
				}, {
					Text:         lang.Button.ScheduleNavigationNextDay,
					CallbackData: "open.schedule.day#date=" + nextDayDate.Format("2006-01-02"),
				}},
				{{
					Text:         lang.Button.ScheduleNavigationPreviousWeek,
					CallbackData: "open.schedule.day#date=" + prevWeekDate.Format("2006-01-02"),
				}, {
					Text:         lang.Button.ScheduleNavigationNextWeek,
					CallbackData: "open.schedule.day#date=" + nextWeekDate.Format("2006-01-02"),
				}},
				{{
					Text:         lang.Button.Menu,
					CallbackData: "open.menu",
				}},
			},
		}

		// Add today button if needed
		if date != time.Now().Format("2006-01-02") {
			buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1] = append(
				buttons.InlineKeyboard[len(buttons.InlineKeyboard)-1],
				gotgbot.InlineKeyboardButton{
					Text:         lang.Button.ScheduleNavigationToday,
					CallbackData: "open.schedule.today",
				},
			)
		}

		// Add extra info button if needed
		if CheckExtraText(day) {
			// Add to the start
			buttons.InlineKeyboard = append(
				[][]gotgbot.InlineKeyboardButton{
					{{
						Text:         lang.Button.ScheduleExtra,
						CallbackData: "open.schedule.extra#date=" + date,
					}},
				},
				buttons.InlineKeyboard...,
			)
		}

		pageText += "`—————————————————————————`"
	}

	page := Page{
		Text:                  pageText,
		ReplyMarkup:           buttons,
		ParseMode:             "MarkdownV2",
		DisableWebPagePreview: true,
	}

	return page, nil
}

// isNoLessons checks if there are no lessons in the given day
func isNoLessons(day *api2.TimeTableDate) bool {
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

func getTeacher(teachersNameFull string, teachersList *teachers.TeachersList) string {
	var teacher string

	// Get first teacher
	teachers2 := strings.Split(teachersNameFull, ", ")
	firstTeacher := teachers2[0]
	teacher = firstTeacher

	// Escape markdown
	teacher = utils.EscapeMarkdownV2(teacher)

	// Get teacher profile link
	profileLink, ok := teachersList.GetLink(firstTeacher)
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
	if len(teachers2) > 1 {
		teacher += " \\+" + strconv.Itoa(len(teachers2)-1)
	}

	return teacher
}

// CheckExtraText checks if there is extra text in any lesson of the given day
func CheckExtraText(day *api2.TimeTableDate) bool {
	for _, lesson := range day.Lessons {
		for _, period := range lesson.Periods {
			if period.ExtraText {
				return true
			}
		}
	}
	return false
}

// ScanEmptyDays scans the days before and after the given date and returns the number of days without lessons
func ScanEmptyDays(days []api2.TimeTableDate, date time.Time) (int, int, error) {
	skipLeft, err := CountNoLessonsDays(days, date, false)
	if err != nil {
		return 0, 0, err
	}

	skipRight, err := CountNoLessonsDays(days, date, true)
	if err != nil {
		return 0, 0, err
	}

	return skipLeft, skipRight, nil
}

// CountNoLessonsDays counts the number of days without lessons
func CountNoLessonsDays(days []api2.TimeTableDate, date time.Time, directionRight bool) (int, error) {
	count := 0

	if directionRight {
		for _, day := range days {
			date_, err := api2.ParseISODate(day.Date)
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
		for i := len(days) - 1; i >= 0; i-- {
			date_, err := api2.ParseISODate(days[i].Date)
			if err != nil {
				return 0, err
			}
			if date_.After(date) {
				continue
			}
			day := days[i]
			if len(day.Lessons) == 0 {
				count++
			} else {
				break
			}
		}
	}

	return count, nil
}

func getLocalizedDate(lang i18n.Language, date time.Time) string {
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
