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

package api

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/op/go-logging"
	"io"
	"net/http"
	"time"
)

var log = logging.MustGetLogger("DefaultApi")

const Location = "Europe/Kyiv"

type DefaultApi struct {
	Url     string
	Timeout time.Duration
}

// Api is a wrapper for mkr.org.ua API requests.
// Documentation can be found here: https://mkr.org.ua
type Api interface {
	// GetStructures returns a list of structures
	GetStructures() ([]Structure, error)
	// GetFaculties returns a list of faculties in a structure
	GetFaculties(structureId int) ([]Faculty, error)
	// GetCourses returns a list of courses in a faculty
	GetCourses(facultyId int) ([]Course, error)
	// GetGroups returns a list of groups in a faculty
	GetGroups(facultyId int, course int) ([]Group, error)
	// GetGroupStudents returns a list of students in a group
	GetGroupStudents(groupId int) ([]Student, error)
	// GetCallSchedule returns a call schedule
	GetCallSchedule() (CallSchedule, error)
	// GetGroupSchedule returns a schedule for a group
	// from dateStart to dateEnd (inclusive)
	GetGroupSchedule(groupId int, dateStart string, dateEnd string) (Schedule, error)
	// GetScheduleExtraInfo returns a extra info for a schedule,
	// that can be added by a teacher or university administration.
	//
	// classCode is a TimeTablePeriod.R1 field
	GetScheduleExtraInfo(classCode int, date string) (ScheduleExtraInfo, error)
	// GetGroupScheduleDay returns a schedule for a group for a day
	//
	// Alias for GetGroupSchedule(groupId, date, date).GetDay(date)
	GetGroupScheduleDay(groupId int, date string) (*TimeTableDate, error)
}

// NewApi creates a new DefaultApi instance
func NewApi(url string) Api {
	return &DefaultApi{
		Url: url,
	}
}

// makeRequest makes a request to the API.
// Needed to avoid code duplication
func (a DefaultApi) makeRequest(method string, path string, body string, result any) error {
	log.Debugf("Making request: %s %s %s", method, path, body)

	// Generate request body
	var reqBody io.Reader
	if body == "" {
		reqBody = nil
	} else {
		reqBody = bytes.NewBuffer([]byte(body))
	}

	req, err := http.NewRequest(method, a.Url+path, reqBody)
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Accept-Language", "uk")
	client := &http.Client{
		Timeout: a.Timeout,
	}

	res, err := client.Do(req)
	if err != nil {
		return err
	}

	resBody, err := io.ReadAll(res.Body)
	if err != nil {
		return err
	}

	if err := res.Body.Close(); err != nil {
		return err
	}

	// Handle non-200 status codes
	if res.StatusCode != http.StatusOK {
		err := &HTTPApiError{Code: res.StatusCode, Body: string(resBody)}

		switch res.StatusCode {
		case http.StatusUnauthorized:
			var e UnauthorizedError
			if err := json.Unmarshal(resBody, &e); err != nil {
				return err
			}
			err.Err = &e
		case http.StatusForbidden:
			var e ForbiddenError
			if err := json.Unmarshal(resBody, &e); err != nil {
				return err
			}
			err.Err = &e
		case http.StatusUnprocessableEntity:
			var e ValidationError
			if err := json.Unmarshal(resBody, &e.Fields); err != nil {
				return err
			}
			err.Err = &e
		case http.StatusInternalServerError:
			var e InternalServerError
			if err := json.Unmarshal(resBody, &e); err != nil {
				return err
			}
			err.Err = &e
		default:
			return err
		}

		return err
	}

	if err := json.Unmarshal(resBody, &result); err != nil {
		return err
	}

	return nil
}

func (a DefaultApi) GetStructures() ([]Structure, error) {
	var structures []Structure

	err := a.makeRequest("GET", "/list/structures", "", &structures)
	if err != nil {
		return nil, err
	}

	return structures, nil
}

func (a DefaultApi) GetFaculties(structureId int) ([]Faculty, error) {
	var faculties []Faculty
	body := fmt.Sprintf(`{"structureId":%d}`, structureId)

	err := a.makeRequest("POST", "/list/faculties", body, &faculties)
	if err != nil {
		return nil, err
	}

	return faculties, nil
}

func (a DefaultApi) GetCourses(facultyId int) ([]Course, error) {
	var courses []Course
	body := fmt.Sprintf(`{"facultyId":%d}`, facultyId)

	err := a.makeRequest("POST", "/list/courses", body, &courses)
	if err != nil {
		return nil, err
	}

	return courses, nil
}

func (a DefaultApi) GetGroups(facultyId int, course int) ([]Group, error) {
	var groups []Group
	body := fmt.Sprintf(`{"facultyId":%d,"course":%d}`, facultyId, course)

	err := a.makeRequest("POST", "/list/groups", body, &groups)
	if err != nil {
		return nil, err
	}

	return groups, nil
}

func (a DefaultApi) GetGroupStudents(groupId int) ([]Student, error) {
	var students []Student
	body := fmt.Sprintf(`{"groupId":%d}`, groupId)

	err := a.makeRequest("POST", "/list/students-by-group", body, &students)
	if err != nil {
		return nil, err
	}

	return students, nil
}

func (a DefaultApi) GetCallSchedule() (CallSchedule, error) {
	var callSchedule []CallScheduleEntry

	err := a.makeRequest("POST", "/time-table/call-schedule", "", &callSchedule)
	if err != nil {
		return nil, err
	}

	return callSchedule, nil
}

func (a DefaultApi) GetGroupSchedule(groupId int, dateStart string, dateEnd string) (Schedule, error) {
	var timeTableDate []TimeTableDate
	body := fmt.Sprintf(`{"groupId":%d,"dateStart":"%s","dateEnd":"%s"}`, groupId, dateStart, dateEnd)

	err := a.makeRequest("POST", "/time-table/group", body, &timeTableDate)
	if err != nil {
		return nil, err
	}

	err = FillEmptyDates(&timeTableDate, dateStart, dateEnd)
	if err != nil {
		return nil, err
	}

	return timeTableDate, nil
}

func (a DefaultApi) GetScheduleExtraInfo(classCode int, date string) (ScheduleExtraInfo, error) {
	var scheduleExtraInfo ScheduleExtraInfo
	body := fmt.Sprintf(`{"r1":%d,"r2":"%s"}`, classCode, date)

	err := a.makeRequest("POST", "/time-table/schedule-ad", body, &scheduleExtraInfo)
	return scheduleExtraInfo, err
}

func (a DefaultApi) GetGroupScheduleDay(groupId int, date string) (*TimeTableDate, error) {
	schedule, err := a.GetGroupSchedule(groupId, date, date)
	if err != nil {
		return nil, err
	}

	return schedule.GetDay(date), err
}
