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

package notifier

import (
	_ "embed"
	"errors"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/errorhandler"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
	"github.com/cubicbyte/dteubot/pkg/api/cachedapi"
	"github.com/go-co-op/gocron"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"github.com/sirkon/go-format/v2"
	"net/url"
	"strings"
	"time"
)

var Location = "Europe/Kiev"

var log = logging.MustGetLogger("Notifier")

var (
	//go:embed sql/get_chats_15m.sql
	getChats15mQuery string
	//go:embed sql/get_chats_1m.sql
	getChats1mQuery string
)

var (
	db        *data.Database
	api       *cachedapi.CachedApi
	bot       *tgbotapi.BotAPI
	langs     map[string]i18n.Language
	calls     api2.CallSchedule
	location  *time.Location
	Scheduler *gocron.Scheduler
)

type chatInfo struct {
	ChatId          int64  `db:"chat_id"`
	GroupId         int    `db:"group_id"`
	LangCode        string `db:"lang_code"`
	ClNotifNextPart bool   `db:"cl_notif_next_part"`
}

// Setup initializes notifier and starts cron Scheduler
func Setup(db2 *data.Database, api3 *cachedapi.CachedApi, bot2 *tgbotapi.BotAPI, langs2 map[string]i18n.Language) error {
	log.Info("Setting up notifier")

	db = db2
	api = api3
	bot = bot2
	langs = langs2

	// Setup cron Scheduler
	var err error
	location, err = time.LoadLocation(Location)
	if err != nil {
		return err
	}
	Scheduler = gocron.NewScheduler(location)

	// Get calls
	calls, err = api.GetCallSchedule()
	if err != nil {
		return err
	}

	// Format calls to cron format
	// Call time = "08:20", then cron time += "08:05;08:19;"
	cronTime15m := ""
	cronTime1m := ""
	for _, call := range calls {
		// Parse call start time
		timeStart, err := time.Parse("15:04", call.TimeStart)
		if err != nil {
			return err
		}

		// 15 minutes
		cronTime15m += timeStart.Add(-15*time.Minute).Format("15:04") + ";"

		// 1 minute
		cronTime1m += timeStart.Add(-1*time.Minute).Format("15:04") + ";"
	}
	// Remove last semicolon
	cronTime15m = cronTime15m[:len(cronTime15m)-1]
	cronTime1m = cronTime1m[:len(cronTime1m)-1]

	// Add cron jobs
	_, err = Scheduler.Every(1).Day().At(cronTime15m).Do(SendNotifications, "15m")
	if err != nil {
		return err
	}
	_, err = Scheduler.Every(1).Day().At(cronTime1m).Do(SendNotifications, "1m")
	if err != nil {
		return err
	}

	return nil
}

// SendNotifications sends notifications to chats that subscribed to notifications
func SendNotifications(time2 string) error {
	log.Infof("Sending notifications %s", time2)

	// Get chats with notifications enabled
	chats, err := GetSubscribedChats(time2)
	if err != nil {
		return err
	}
	log.Debugf("Got %d chats with notifications enabled", len(chats))

	// Get current time
	curTime := time.Now().In(location)

	// Send notifications
	sentCount := 0
	for _, chat := range chats {
		// Get group schedule
		schedule, err := api.GetGroupScheduleDay(chat.GroupId, curTime.Format("2006-01-02"))
		if err != nil {
			// Check if user blocked bot
			var tgError *tgbotapi.Error
			if errors.As(err, &tgError) && tgError.Code == 403 {
				// User blocked bot
				log.Infof("Bot blocked in chat %d", chat.ChatId)
				if err = MakeChatUnavailable(chat.ChatId); err != nil {
					log.Errorf("Error making chat %d unavailable: %s", chat.ChatId, err)
					errorhandler.SendErrorToTelegram(err)
				}
				continue
			}

			// Check if api connection error
			var urlError *url.Error
			if errors.As(err, &urlError) {
				log.Warningf("Error getting result from API for chat %d: %s", chat.ChatId, err)
				continue
			}

			// Unknown error
			log.Errorf("Error getting group schedule day for chat %d: %s", chat.ChatId, err)
			errorhandler.SendErrorToTelegram(err)
			continue
		}

		// Check if group have classes
		haveClasses, err := IsGroupHaveClasses(schedule, curTime)
		if err != nil {
			log.Errorf("Error checking if group have classes for chat %d: %s", chat.ChatId, err)
			errorhandler.SendErrorToTelegram(err)
			continue
		}

		if haveClasses {
			// Group have classes, send notification

			// Send notification to chat
			err = SendNotification(chat.ChatId, chat.LangCode, schedule, time2, "start")
			if err != nil {
				log.Warningf("Error sending notification to chat %d: %s", chat.ChatId, err)
				errorhandler.SendErrorToTelegram(err)
				continue
			}

			sentCount++
			continue
		}

		// Check if group have next classes part
		if !chat.ClNotifNextPart {
			continue
		}

		haveNextClassesPart, err := IsGroupHaveNextClassesPart(schedule, curTime)
		if err != nil {
			log.Errorf("Error checking if group have next classes part for chat %d: %s", chat.ChatId, err)
			errorhandler.SendErrorToTelegram(err)
			continue
		}

		if haveNextClassesPart {
			// Group have next classes part, send notification

			// Send notification to chat
			err = SendNotification(chat.ChatId, chat.LangCode, schedule, time2, "next_part")
			if err != nil {
				log.Warningf("Error sending notification to chat %d: %s", chat.ChatId, err)
				errorhandler.SendErrorToTelegram(err)
				continue
			}

			sentCount++
			continue
		}
	}

	log.Infof("Sent notifications to %d chats", sentCount)

	return nil
}

// SendNotification sends notification to chat
func SendNotification(chatId int64, langCode string, schedule *api2.TimeTableDate, time string, type2 string) error {
	log.Debugf("Sending %s %s notification to chat %d", type2, time, chatId)

	// Get chat language
	lang, ok := langs[langCode]
	if !ok {
		return &i18n.LanguageNotFoundError{LangCode: langCode}
	}

	var pageText string
	if type2 == "start" {
		// Create page schedule section
		section := ""
		strFormat := "`$lesson\\)` *$name*`[$type]`\n"
		for _, lesson := range schedule.Lessons {
			for _, period := range lesson.Periods {
				section += format.Formatm(strFormat, format.Values{
					"lesson": lesson.Number,
					"name":   utils.EscapeText(tgbotapi.ModeMarkdownV2, period.DisciplineShortName),
					"type":   utils.EscapeText(tgbotapi.ModeMarkdownV2, period.TypeStr),
				})
			}
		}

		// Create page text
		pageText = format.Formatm(lang.Page.ClassesNotification, format.Values{
			"remaining": time[:len(time)-1], // Remove last letter: 15m -> 15
			"schedule":  section,
		})
	} else if type2 == "next_part" {
		// Create page text
		pageText = format.Formatm(lang.Page.ClassesNotificationNextPart, format.Values{
			"remaining": time[:len(time)-1],
		})
	} else {
		return errors.New("invalid notification type: " + type2)
	}

	// Create buttons
	replyMarkup := tgbotapi.NewInlineKeyboardMarkup(
		tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(lang.Button.OpenSchedule, "open.schedule.day#from=notification&date="+schedule.Date),
			tgbotapi.NewInlineKeyboardButtonData(lang.Button.Settings, "open.settings#from=notification"),
		),
	)

	// Send message
	msg := tgbotapi.NewMessage(chatId, pageText)
	msg.ParseMode = tgbotapi.ModeMarkdownV2
	msg.ReplyMarkup = replyMarkup

	_, err := bot.Send(msg)
	if err != nil {
		return err
	}

	return nil
}

// GetSubscribedChats returns chats that subscribed to notifications for given time
func GetSubscribedChats(time string) ([]chatInfo, error) {
	chats := make([]chatInfo, 0)
	var err error

	switch time {
	case "15m":
		err = db.Db.Select(&chats, getChats15mQuery)
	case "1m":
		err = db.Db.Select(&chats, getChats1mQuery)
	default:
		panic("invalid time: " + time)
	}

	if err != nil {
		return nil, err
	}

	return chats, nil
}

// IsGroupHaveClasses checks if group have classes at given time that are about to start
// to know if we need to send notifications
func IsGroupHaveClasses(schedule *api2.TimeTableDate, time2 time.Time) (bool, error) {
	// Get first lesson
	if len(schedule.Lessons) == 0 {
		return false, nil
	}
	firstLesson := schedule.Lessons[0]

	// Check if first lesson is actually first lesson
	// Needed because university can add lesson like "приховано з **"
	// Can be removed if it is not the case anymore
	lessonName := strings.ToLower(firstLesson.Periods[0].DisciplineShortName)
	if strings.Contains(lessonName, "приховано") {
		return false, nil
	}

	// Check if first lesson is about to start
	return isLessonIsAboutToStart(&firstLesson, time2)
}

// IsGroupHaveNextClassesPart checks if group have next classes part
// at given time that are about to start.
func IsGroupHaveNextClassesPart(schedule *api2.TimeTableDate, time2 time.Time) (bool, error) {
	if len(schedule.Lessons) == 0 {
		return false, nil
	}

	// Get previous and next lesson
	var previousLesson *api2.TimeTableLesson
	var nextLesson *api2.TimeTableLesson
	for i, lesson := range schedule.Lessons {
		timeEnd, err := time.Parse("15:04", lesson.Periods[0].TimeEnd)
		timeEnd = time.Date(time2.Year(), time2.Month(), time2.Day(), timeEnd.Hour(), timeEnd.Minute(), 0, 0, location)
		if err != nil {
			return false, err
		}

		if time2.Before(timeEnd) {
			if i != 0 {
				previousLesson = schedule.GetLesson(lesson.Number - 1)
			}
			nextLesson = &lesson
			break
		}
	}

	// If there is no next lesson, return false
	if nextLesson == nil {
		return false, nil
	}

	// If it's first lesson of the day
	if previousLesson == nil {
		return isLessonIsAboutToStart(nextLesson, time2)
	}

	// Check if next lesson have new discipline
	for _, nextPeriod := range nextLesson.Periods {
		for _, prevPeriod := range previousLesson.Periods {
			if prevPeriod.R1 == nextPeriod.R1 {
				return false, nil
			}
		}
	}

	return isLessonIsAboutToStart(nextLesson, time2)
}

// isLessonIsAboutToStart checks if lesson is about to start
func isLessonIsAboutToStart(lesson *api2.TimeTableLesson, time2 time.Time) (bool, error) {
	// Get this lesson call and previous lesson call
	var thisCall *api2.CallScheduleEntry
	var previousCall *api2.CallScheduleEntry
	for i, call := range calls {
		if call.Number == lesson.Number {
			thisCall = &call
			if i != 0 {
				previousCall = &calls[i-1]
			}
			break
		}
	}

	if thisCall == nil {
		log.Errorf("Error getting current call for lesson %d", lesson.Number)
		return false, nil
	}

	// Get this call end time and previous call end time
	thisCallEndTime, err := time.Parse("15:04", thisCall.TimeEnd)
	if err != nil {
		return false, err
	}
	thisCallEndTime = time.Date(time2.Year(), time2.Month(), time2.Day(), thisCallEndTime.Hour(), thisCallEndTime.Minute(), 0, 0, location)

	var previousCallEndTime time.Time
	if previousCall == nil {
		// If there is no previous call, happens only on first call of the day
		previousCallEndTime = time2.Add(-1 * time.Minute)
	} else {
		previousCallEndTime, err = time.Parse("15:04", previousCall.TimeEnd)
		if err != nil {
			return false, err
		}
		previousCallEndTime = time.Date(time2.Year(), time2.Month(), time2.Day(), previousCallEndTime.Hour(), previousCallEndTime.Minute(), 0, 0, location)
	}

	// So, to check if lesson is about to start we need to check
	// if current time is between previous call end and this call end
	if time2.After(previousCallEndTime) && time2.Before(thisCallEndTime) {
		return true, nil
	}

	return false, nil
}

// MakeChatUnavailable makes chat unavailable if user blocked bot.
// It is needed to prevent sending notifications to blocked users.
func MakeChatUnavailable(chatId int64) error {
	cm := data.ChatDataManager{ChatId: chatId, Database: db}
	chatData, err := cm.GetChatData()
	if err != nil {
		return err
	}

	chatData.Accessible = false
	err = cm.UpdateChatData(chatData)
	if err != nil {
		return err
	}

	return nil
}
