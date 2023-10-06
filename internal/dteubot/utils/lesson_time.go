package utils

import (
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
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
func GetCallsStatus(groupId int, time_ time.Time) (*CallsStatus, error) {
	calls, err := settings.Api.GetCallSchedule()
	if err != nil {
		return nil, err
	}

	date := time_
	for i := 0; i < DaysScanLimit; i++ {
		day, err := settings.Api.GetGroupScheduleDay(groupId, date.Format("2006-01-02"))
		if err != nil {
			return nil, err
		}

		status, err := getCallsStatus(*day, calls, time_)
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
func getCallsStatus(day api.TimeTableDate, calls []api.CallSchedule, time_ time.Time) (*CallsStatus, error) {
	if len(day.Lessons) == 0 {
		return nil, nil
	}

	// Check if the current time is before the first lesson
	firstCall := GetCall(&calls, day.Lessons[0].Number)
	firstCallStart, err := ParseTime("2006-01-02 15:04", day.Date+" "+firstCall.TimeStart)
	if err != nil {
		return nil, err
	}
	if time_.Before(firstCallStart) {
		return &CallsStatus{
			Status: CallStatusBeforeStart,
			Time:   firstCallStart,
		}, nil
	}

	// Check if the current time is after the last lesson
	lastCall := GetCall(&calls, day.Lessons[len(day.Lessons)-1].Number)
	lastCallEnd, err := ParseTime("2006-01-02 15:04", day.Date+" "+lastCall.TimeEnd)
	if err != nil {
		return nil, err
	}
	if time_.After(lastCallEnd) {
		return nil, nil
	}

	// Check if the current time is during the lesson or break
	for _, lesson := range day.Lessons {
		call := GetCall(&calls, lesson.Number)
		callStart, err := ParseTime("2006-01-02 15:04", day.Date+" "+call.TimeStart)
		if err != nil {
			return nil, err
		}
		callEnd, err := ParseTime("2006-01-02 15:04", day.Date+" "+call.TimeEnd)
		if err != nil {
			return nil, err
		}

		// Check if the current time is during the lesson
		if time_.After(callStart) && time_.Before(callEnd) {
			return &CallsStatus{
				Status: CallStatusDuring,
				Time:   callEnd,
			}, nil
		}

		// Check if the current time is before the next lesson
		if time_.Before(callStart) {
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
func FormatDuration(duration time.Duration, depth int, lang *i18n.Language) string {
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

func GetCall(calls *[]api.CallSchedule, number int) *api.CallSchedule {
	for _, call := range *calls {
		if call.Number == number {
			return &call
		}
	}
	return nil
}
