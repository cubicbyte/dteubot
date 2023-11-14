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

package utils

import (
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	"strconv"
	"time"
)

type CallStatusType int8

const (
	// CallStatusBeforeStart - before the first lesson
	CallStatusBeforeStart CallStatusType = iota
	// CallStatusBefore - before the next lesson (time when break ends)
	CallStatusBefore
	// CallStatusDuring - during the lesson
	CallStatusDuring
)

type CallsStatus struct {
	Status CallStatusType
	Time   time.Time
}

// DaysScanLimit - limit of days to scan for the start of the next lesson in /left command
const DaysScanLimit = 7

// GetCallsStatus returns the time relative to the current lesson
func GetCallsStatus(groupId int, time2 time.Time, api2 api.IApi) (*CallsStatus, error) {
	calls, err := api2.GetCallSchedule()
	if err != nil {
		return nil, err
	}

	dateStart := time2.Format("2006-01-02")
	dateEnd := time2.AddDate(0, 0, DaysScanLimit).Format("2006-01-02")
	schedule, err := api2.GetGroupSchedule(groupId, dateStart, dateEnd)
	if err != nil {
		return nil, err
	}

	date := time2
	for i := 0; i < DaysScanLimit; i++ {
		day := schedule.GetDay(date.Format("2006-01-02"))
		if day == nil {
			date = date.AddDate(0, 0, 1)
			continue
		}

		status, err := getCallsStatus(*day, calls, time2)
		if err != nil {
			return nil, err
		}

		if status != nil {
			return status, nil
		}

		date = date.AddDate(0, 0, 1)
	}

	return nil, nil
}

// getCallsStatus returns GetCallsStatus for a specific day
func getCallsStatus(day api.TimeTableDate, calls api.CallSchedule, time2 time.Time) (*CallsStatus, error) {
	if len(day.Lessons) == 0 {
		return nil, nil
	}

	// Check if the current time is before the first lesson
	firstCall := calls.GetCall(day.Lessons[0].Number)
	firstCallStart, err := time.Parse("2006-01-02 15:04", day.Date+" "+firstCall.TimeStart)
	if err != nil {
		return nil, err
	}

	firstCallStart = SetLocation(firstCallStart, time2.Location())

	if time2.Before(firstCallStart) {
		return &CallsStatus{
			Status: CallStatusBeforeStart,
			Time:   firstCallStart,
		}, nil
	}

	// Check if the current time is after the last lesson
	lastCall := calls.GetCall(day.Lessons[len(day.Lessons)-1].Number)
	lastCallEnd, err := time.Parse("2006-01-02 15:04", day.Date+" "+lastCall.TimeEnd)
	if err != nil {
		return nil, err
	}

	lastCallEnd = SetLocation(lastCallEnd, time2.Location())

	if time2.After(lastCallEnd) {
		return nil, nil
	}

	// Check if the current time is during the lesson or break
	for _, lesson := range day.Lessons {
		call := calls.GetCall(lesson.Number)

		callStart, err := time.Parse("2006-01-02 15:04", day.Date+" "+call.TimeStart)
		if err != nil {
			return nil, err
		}
		callStart = SetLocation(callStart, time2.Location())

		callEnd, err := time.Parse("2006-01-02 15:04", day.Date+" "+call.TimeEnd)
		if err != nil {
			return nil, err
		}
		callEnd = SetLocation(callEnd, time2.Location())

		// Check if the current time is during the lesson
		if time2.After(callStart) && time2.Before(callEnd) {
			return &CallsStatus{
				Status: CallStatusDuring,
				Time:   callEnd,
			}, nil
		}

		// Check if the current time is before the next lesson
		if time2.Before(callStart) {
			return &CallsStatus{
				Status: CallStatusBefore,
				Time:   callStart,
			}, nil
		}
	}

	return nil, nil
}

// FormatDuration formats time.Duration into a readable format
//
// Example:
// FormatDuration(duration, depth=2) // "2d. 9h."
func FormatDuration(duration time.Duration, depth int, lang i18n.Language) string {
	result := ""
	curDepth := 0

	if duration.Hours() >= 24 {
		result += strconv.Itoa(int(duration.Hours()/24)) + " " + lang.Text.ShortTimeDays + " "
		duration -= time.Duration(int(duration.Hours()/24)) * 24 * time.Hour
		curDepth++
	}

	if curDepth < depth && duration.Hours() >= 1 {
		result += strconv.Itoa(int(duration.Hours())) + " " + lang.Text.ShortTimeHours + " "
		duration -= time.Duration(int(duration.Hours())) * time.Hour
		curDepth++
	}

	if curDepth < depth && duration.Minutes() >= 1 {
		result += strconv.Itoa(int(duration.Minutes())) + " " + lang.Text.ShortTimeMinutes + " "
		duration -= time.Duration(int(duration.Minutes())) * time.Minute
		curDepth++
	}

	if curDepth < depth && duration.Seconds() >= 1 {
		result += strconv.Itoa(int(duration.Seconds())) + " " + lang.Text.ShortTimeSeconds + " "
		curDepth++
	}

	// Remove last space
	if result != "" {
		result = result[:len(result)-1]
	}

	return result
}
