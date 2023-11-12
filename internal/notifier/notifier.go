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
	"context"
	_ "embed"
	"errors"
	"fmt"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/errorhandler"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
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

// Setup initializes notifier and starts cron Scheduler
func Setup(ctx context.Context, api api2.IApi, bot *gotgbot.Bot, langs map[string]i18n.Language, chatRepo data.ChatRepository) (*gocron.Scheduler, error) {
	log.Info("Setting up notifier")

	// Setup cron scheduler
	var err error
	location, err := time.LoadLocation(Location)
	if err != nil {
		return nil, err
	}
	scheduler := gocron.NewScheduler(location)

	// Get calls
	calls, err := api.GetCallSchedule()
	if err != nil {
		return nil, err
	}

	// Format calls to cron format
	// Call time = "08:20", then cron time += "08:05;08:19;"
	cronTime15m := ""
	cronTime1m := ""
	for _, call := range calls {
		// Parse call start time
		timeStart, err := time.Parse("15:04", call.TimeStart)
		if err != nil {
			return nil, err
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
	_, err = scheduler.Every(1).Day().At(cronTime15m).Do(SendNotifications, ctx, "15m", chatRepo, api, bot, langs, calls)
	if err != nil {
		return nil, err
	}
	_, err = scheduler.Every(1).Day().At(cronTime1m).Do(SendNotifications, ctx, "1m", chatRepo, api, bot, langs, calls)
	if err != nil {
		return nil, err
	}

	return scheduler, nil
}

// SendNotifications sends notifications to chats that subscribed to notifications
func SendNotifications(ctx context.Context, time2 string, chatRepo data.ChatRepository, api api2.IApi, bot *gotgbot.Bot, langs map[string]i18n.Language, calls api2.CallSchedule) error {
	log.Infof("Sending notifications %s", time2)

	// TODO: Limit message sending per second

	// Get chats with notifications enabled
	chats, err := GetSubscribedChats(time2, chatRepo)
	if err != nil {
		return err
	}
	log.Debugf("Got %d chats with notifications enabled", len(chats))

	loc, err := time.LoadLocation(Location)
	if err != nil {
		return err
	}

	// Get current time
	curTime := time.Now().In(loc)

	// Send notifications
	sentCount := 0
	for _, chat := range chats {
		// Get group schedule
		schedule, err := api.GetGroupScheduleDay(chat.GroupId, curTime.Format(time.DateOnly))
		if err != nil {
			// Check if api connection error
			var urlError *url.Error
			if errors.As(err, &urlError) {
				log.Warningf("Error getting result from API for chat %d: %s", chat.Id, err)
				continue
			}

			// Unknown error
			log.Errorf("Error getting group schedule day for chat %d: %s", chat.Id, err)
			errorhandler.SendErrorToTelegram(ctx, err, bot)
			continue
		}

		// Check if group have classes
		expectedTime := AddNotificationTime(curTime, time2)
		haveClasses, err := IsGroupHaveClasses(schedule, calls, expectedTime)
		if err != nil {
			log.Errorf("Error checking if group have classes for chat %d: %s", chat.Id, err)
			errorhandler.SendErrorToTelegram(ctx, err, bot)
			continue
		}

		if haveClasses {
			// Group have classes, send notification

			// Get chat language
			lang, err := utils.GetLang(chat.LanguageCode, langs)
			if err != nil {
				log.Errorf("Error getting language for chat %d: %s", chat.Id, err)
				errorhandler.SendErrorToTelegram(ctx, err, bot)
				continue
			}

			// Send notification to chat
			err = SendNotification(ctx, chat, chatRepo, lang, bot, schedule, time2, "start")
			if err != nil {
				log.Warningf("Error sending notification to chat %d: %s", chat.Id, err)
				errorhandler.SendErrorToTelegram(ctx, err, bot)
				continue
			}

			sentCount++
			continue
		}

		// Check if group have next classes part
		if !chat.ClassesNotificationNextPart {
			continue
		}

		haveNextClassesPart, err := IsGroupHaveNextClassesPart(schedule, calls, expectedTime)
		if err != nil {
			log.Errorf("Error checking if group have next classes part for chat %d: %s", chat.Id, err)
			errorhandler.SendErrorToTelegram(ctx, err, bot)
			continue
		}

		if haveNextClassesPart {
			// Group have next classes part, send notification

			// Get chat language
			lang, err := utils.GetLang(chat.LanguageCode, langs)
			if err != nil {
				log.Errorf("Error getting language for chat %d: %s", chat.Id, err)
				errorhandler.SendErrorToTelegram(ctx, err, bot)
				continue
			}

			// Send notification to chat
			err = SendNotification(ctx, chat, chatRepo, lang, bot, schedule, time2, "next_part")
			if err != nil {
				log.Warningf("Error sending notification to chat %d: %s", chat.Id, err)
				errorhandler.SendErrorToTelegram(ctx, err, bot)
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
func SendNotification(ctx context.Context, chat *data.Chat, chatRepo data.ChatRepository, lang *i18n.Language, bot *gotgbot.Bot, schedule *api2.TimeTableDate, time string, type2 string) error {
	log.Debugf("Sending %s %s notification to chat %d", type2, time, chat.Id)

	var pageText string
	if type2 == "start" {
		// Create page schedule section
		section := ""
		strFormat := "`$lesson\\)` *$name*`[$type]`\n"
		for _, lesson := range schedule.Lessons {
			for _, period := range lesson.Periods {
				section += format.Formatm(strFormat, format.Values{
					"lesson": lesson.Number,
					"name":   utils.EscapeMarkdownV2(period.DisciplineShortName),
					"type":   utils.EscapeMarkdownV2(period.TypeStr),
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
	replyMarkup := gotgbot.InlineKeyboardMarkup{
		InlineKeyboard: [][]gotgbot.InlineKeyboardButton{{
			{
				Text:         lang.Button.OpenSchedule,
				CallbackData: "open.schedule.day#from=notification&date=" + schedule.Date,
			}, {
				Text:         lang.Button.Settings,
				CallbackData: "open.settings#from=notification",
			},
		}},
	}

	// Send message
	opts := gotgbot.SendMessageOpts{
		ParseMode:   gotgbot.ParseModeMarkdownV2,
		ReplyMarkup: replyMarkup,
	}

	_, err := bot.SendMessage(chat.Id, pageText, &opts)
	if err != nil {
		// Check if user blocked bot
		var tgError *tgbotapi.Error
		if errors.As(err, &tgError) && tgError.Code == 403 {
			log.Infof("Bot blocked in chat %d", chat.Id)
			if err = MakeChatUnavailable(chat, chatRepo); err != nil {
				log.Errorf("Error making chat %d unavailable: %s", chat.Id, err)
				errorhandler.SendErrorToTelegram(ctx, err, bot)
			}
			return nil
		}

		return err
	}

	return nil
}

// GetSubscribedChats returns chats that subscribed to notifications for given time
func GetSubscribedChats(time string, chatRepo data.ChatRepository) ([]*data.Chat, error) {
	switch time {
	case "15m":
		return chatRepo.GetChatsWithEnabled15mNotification()
	case "1m":
		return chatRepo.GetChatsWithEnabled1mNotification()
	default:
		return nil, fmt.Errorf("invalid time: %s", time)
	}
}

// IsGroupHaveClasses checks if group have classes at given time that are about to start
// to know if we need to send notifications
func IsGroupHaveClasses(schedule *api2.TimeTableDate, calls api2.CallSchedule, time2 time.Time) (bool, error) {
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
	return isLessonIsAboutToStart(&firstLesson, calls, time2)
}

// IsGroupHaveNextClassesPart checks if group have next classes part
// at given time that are about to start.
func IsGroupHaveNextClassesPart(schedule *api2.TimeTableDate, calls api2.CallSchedule, time2 time.Time) (bool, error) {
	if len(schedule.Lessons) == 0 {
		return false, nil
	}

	// Get previous and next lesson
	var previousLesson *api2.TimeTableLesson
	var nextLesson *api2.TimeTableLesson
	for i, lesson := range schedule.Lessons {
		timeEnd, err := time.Parse("15:04", lesson.Periods[0].TimeEnd)
		timeEnd = time.Date(time2.Year(), time2.Month(), time2.Day(), timeEnd.Hour(), timeEnd.Minute(), 0, 0, time2.Location())
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
		return isLessonIsAboutToStart(nextLesson, calls, time2)
	}

	// Check if next lesson have new discipline
	for _, nextPeriod := range nextLesson.Periods {
		for _, prevPeriod := range previousLesson.Periods {
			if prevPeriod.R1 == nextPeriod.R1 {
				return false, nil
			}
		}
	}

	return isLessonIsAboutToStart(nextLesson, calls, time2)
}

// isLessonIsAboutToStart checks if lesson is about to start
func isLessonIsAboutToStart(lesson *api2.TimeTableLesson, calls api2.CallSchedule, time2 time.Time) (bool, error) {
	// Get this lesson call and previous lesson call
	thisCall := calls.GetCall(lesson.Number)
	previousCall := calls.GetCall(lesson.Number - 1)

	if thisCall == nil {
		log.Errorf("Error getting current call for lesson %d", lesson.Number)
		return false, nil
	}

	// Get this call end time and previous call end time
	thisCallEndTime, err := time.Parse("15:04", thisCall.TimeEnd)
	if err != nil {
		return false, err
	}
	thisCallEndTime = time.Date(time2.Year(), time2.Month(), time2.Day(), thisCallEndTime.Hour(), thisCallEndTime.Minute(), 0, 0, time2.Location())

	var previousCallEndTime time.Time
	if previousCall == nil {
		// If there is no previous call, happens only on first call of the day
		previousCallEndTime = time2.Add(-1 * time.Minute)
	} else {
		previousCallEndTime, err = time.Parse("15:04", previousCall.TimeEnd)
		if err != nil {
			return false, err
		}
		previousCallEndTime = time.Date(time2.Year(), time2.Month(), time2.Day(), previousCallEndTime.Hour(), previousCallEndTime.Minute(), 0, 0, time2.Location())
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
func MakeChatUnavailable(chat *data.Chat, chatRepo data.ChatRepository) error {
	chat.Accessible = false

	if err := chatRepo.Update(chat); err != nil {
		return err
	}

	return nil
}

// AddNotificationTime returns adds notification time to given time
func AddNotificationTime(time2 time.Time, notificationTime string) time.Time {
	switch notificationTime {
	case "15m":
		return time2.Add(15 * time.Minute)
	case "1m":
		return time2.Add(1 * time.Minute)
	default:
		return time2
	}
}
