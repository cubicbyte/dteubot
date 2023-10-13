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

var log = logging.MustGetLogger("api")

const Location = "Europe/Kiev"

// Api is a wrapper for mkr.org.ua API requests.
// Documentation can be found here: https://mkr.org.ua
type Api struct {
	Url     string
	Timeout time.Duration
}

type IApi interface {
	GetStructures() ([]Structure, error)
	GetFaculties(structureId int) ([]Faculty, error)
	GetCourses(facultyId int) ([]Course, error)
	GetGroups(facultyId int, course int) ([]Group, error)
	GetGroupStudents(groupId int) ([]Student, error)
	GetCallSchedule() ([]CallSchedule, error)
	GetGroupSchedule(groupId int, dateStart string, dateEnd string) ([]TimeTableDate, error)
	GetScheduleExtraInfo(classCode int, date string) (*ScheduleExtraInfo, error)
	GetGroupScheduleDay(groupId int, date string) (*TimeTableDate, error)
}

// makeRequest makes a request to the API.
// Needed to avoid code duplication
func (api *Api) makeRequest(method string, path string, body string, result any) error {
	log.Debugf("Making request: %s %s %s", method, path, body)

	// Generate request body
	var reqBody io.Reader
	if body == "" {
		reqBody = nil
	} else {
		reqBody = bytes.NewBuffer([]byte(body))
	}

	req, err := http.NewRequest(method, api.Url+path, reqBody)
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "application/json")
	req.Header.Set("Accept-Language", "uk")
	client := &http.Client{
		Timeout: api.Timeout,
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

// GetStructures returns a list of structures
func (api *Api) GetStructures() ([]Structure, error) {
	var structures []Structure

	err := api.makeRequest("GET", "/list/structures", "", &structures)
	if err != nil {
		return nil, err
	}

	return structures, nil
}

// GetFaculties returns a list of faculties in a structure
func (api *Api) GetFaculties(structureId int) ([]Faculty, error) {
	var faculties []Faculty
	body := fmt.Sprintf(`{"structureId":%d}`, structureId)

	err := api.makeRequest("POST", "/list/faculties", body, &faculties)
	if err != nil {
		return nil, err
	}

	return faculties, nil
}

// GetCourses returns a list of courses in a faculty
func (api *Api) GetCourses(facultyId int) ([]Course, error) {
	var courses []Course
	body := fmt.Sprintf(`{"facultyId":%d}`, facultyId)

	err := api.makeRequest("POST", "/list/courses", body, &courses)
	if err != nil {
		return nil, err
	}

	return courses, nil
}

// GetGroups returns a list of groups in a faculty
func (api *Api) GetGroups(facultyId int, course int) ([]Group, error) {
	var groups []Group
	body := fmt.Sprintf(`{"facultyId":%d,"course":%d}`, facultyId, course)

	err := api.makeRequest("POST", "/list/groups", body, &groups)
	if err != nil {
		return nil, err
	}

	return groups, nil
}

// GetGroupStudents returns a list of students in a group
func (api *Api) GetGroupStudents(groupId int) ([]Student, error) {
	var students []Student
	body := fmt.Sprintf(`{"groupId":%d}`, groupId)

	err := api.makeRequest("POST", "/list/students-by-group", body, &students)
	if err != nil {
		return nil, err
	}

	return students, nil
}

// GetCallSchedule returns a call schedule
func (api *Api) GetCallSchedule() ([]CallSchedule, error) {
	var callSchedule []CallSchedule

	err := api.makeRequest("POST", "/time-table/call-schedule", "", &callSchedule)
	if err != nil {
		return nil, err
	}

	return callSchedule, nil
}

// GetGroupSchedule returns a schedule for a group
// from dateStart to dateEnd (inclusive)
func (api *Api) GetGroupSchedule(groupId int, dateStart string, dateEnd string) ([]TimeTableDate, error) {
	var timeTableDate []TimeTableDate
	body := fmt.Sprintf(`{"groupId":%d,"dateStart":"%s","dateEnd":"%s"}`, groupId, dateStart, dateEnd)

	err := api.makeRequest("POST", "/time-table/group", body, &timeTableDate)
	if err != nil {
		return nil, err
	}

	err = FillEmptyDates(&timeTableDate, dateStart, dateEnd)
	if err != nil {
		return nil, err
	}

	return timeTableDate, nil
}

// GetScheduleExtraInfo returns a extra info for a schedule,
// that can be added by a teacher or university administration.
//
// classCode is a "R1" field from TimeTablePeriod
func (api *Api) GetScheduleExtraInfo(classCode int, date string) (*ScheduleExtraInfo, error) {
	var scheduleExtraInfo ScheduleExtraInfo
	body := fmt.Sprintf(`{"r1":%d,"r2":"%s"}`, classCode, date)

	err := api.makeRequest("POST", "/time-table/schedule-ad", body, &scheduleExtraInfo)
	if err != nil {
		return nil, err
	}

	return &scheduleExtraInfo, nil
}

// GetGroupScheduleDay returns a schedule for a group for a day
//
// Alias for GetGroupSchedule(groupId, date, date)[0]
func (api *Api) GetGroupScheduleDay(groupId int, date string) (*TimeTableDate, error) {
	schedule, err := api.GetGroupSchedule(groupId, date, date)
	if err != nil {
		return nil, err
	}

	// We are not using schedule[0] because api sometimes can return
	// more than one day although we requested only one
	for _, day := range schedule {
		if day.Date == date {
			return &day, nil
		}
	}

	return nil, nil
}