package cachedapi

import (
	"bytes"
	"context"
	"database/sql"
	_ "embed"
	"encoding/binary"
	"encoding/json"
	"fmt"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
	"github.com/gregjones/httpcache/leveldbcache"
	"github.com/op/go-logging"
	"io"
	_ "modernc.org/sqlite"
	"net/http"
	"time"
)

var log = logging.MustGetLogger("api")

// Load embedded SQL files
//
//go:embed sql/setup.sql
var setupSql string

//go:embed sql/get_schedule.sql
var getScheduleSql string

//go:embed sql/update_schedule.sql
var updateScheduleSql string

type CachedApi struct {
	Url             string
	Expires         time.Duration
	Timeout         time.Duration
	cache           *leveldbcache.Cache
	db              *sql.DB
	conn            *sql.Conn
	api             *api2.Api
	getScheduleStmt *sql.Stmt
}

type CachedDate struct {
	GroupId int    `db:"group_id"`
	Date    string `db:"date"`
	Lessons string `db:"lessons"`
	Updated int64  `db:"updated"`
}

func New(url string, leveldbPath string, cachePath string, expires time.Duration, timeout time.Duration) (*CachedApi, error) {
	cache, err := leveldbcache.New(leveldbPath)
	if err != nil {
		return nil, err
	}

	// Create sqlite3 connection
	db, err := sql.Open("sqlite", cachePath)
	if err != nil {
		return nil, err
	}

	// Setup sqlite3 database
	// TODO: Use sqlx
	if _, err := db.Exec(setupSql); err != nil {
		return nil, err
	}

	conn, err := db.Conn(context.Background())
	if err != nil {
		return nil, err
	}

	stmt, err := conn.PrepareContext(context.Background(), getScheduleSql)
	if err != nil {
		return nil, err
	}

	return &CachedApi{
		Url:     url,
		Expires: expires,
		Timeout: timeout,
		cache:   cache,
		db:      db,
		conn:    conn,
		api: &api2.Api{
			Url:     url,
			Timeout: timeout,
		},
		getScheduleStmt: stmt,
	}, nil
}

func (api *CachedApi) Close() error {
	return api.db.Close()
}

func (api *CachedApi) makeRequest(method string, path string, body string, result any) error {
	log.Debugf("Making request: %s %s %s", method, path, body)

	// Get response from cache
	key := method + path + body
	createdKey := "created-" + key
	respBody, respOk := api.cache.Get(key)
	created, createdOk := api.cache.Get(createdKey)

	if respOk && createdOk {
		log.Debug("Got response from cache")

		// Check if response is expired
		createdInt := binary.BigEndian.Uint64(created)
		createdTime := time.Unix(int64(createdInt), 0)

		if time.Since(createdTime) > api.Expires {
			log.Debug("Response is expired")
			api.cache.Delete(key)
			api.cache.Delete(createdKey)
		} else {
			// Return cached response
			if err := json.Unmarshal(respBody, &result); err != nil {
				return err
			}
			return nil
		}
	}

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

	resp, err := client.Do(req)
	if err != nil {
		if respOk {
			// Return cached response if request failed
			log.Warningf("Error making request, using cached result: %s", err)
			if err := json.Unmarshal(respBody, &result); err != nil {
				return err
			}
			return nil
		}
		return err
	}

	resBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return err
	}

	if err := resp.Body.Close(); err != nil {
		return err
	}

	// Handle non-200 status codes
	if resp.StatusCode != http.StatusOK {
		err := &api2.HTTPApiError{Code: resp.StatusCode, Body: string(resBody)}

		switch resp.StatusCode {
		case http.StatusUnauthorized:
			var e api2.UnauthorizedError
			if err := json.Unmarshal(resBody, &e); err != nil {
				return err
			}
			err.Err = &e
		case http.StatusForbidden:
			var e api2.ForbiddenError
			if err := json.Unmarshal(resBody, &e); err != nil {
				return err
			}
			err.Err = &e
		case http.StatusUnprocessableEntity:
			var e api2.ValidationError
			if err := json.Unmarshal(resBody, &e.Fields); err != nil {
				return err
			}
			err.Err = &e
		case http.StatusInternalServerError:
			var e api2.InternalServerError
			if err := json.Unmarshal(resBody, &e); err != nil {
				return err
			}
			err.Err = &e
		default:
			return err
		}

		return err
	}

	// Save response to cache
	now := time.Now().Unix()
	createdBytes := make([]byte, 8)
	binary.BigEndian.PutUint64(createdBytes, uint64(now))
	api.cache.Set(key, resBody)
	api.cache.Set(createdKey, createdBytes)

	if err := json.Unmarshal(resBody, &result); err != nil {
		return err
	}

	return nil
}

// GetStructures returns a list of structures
func (api *CachedApi) GetStructures() ([]api2.Structure, error) {
	var structures []api2.Structure

	err := api.makeRequest("GET", "/list/structures", "", &structures)
	if err != nil {
		return nil, err
	}

	return structures, nil
}

// GetFaculties returns a list of faculties in a structure
func (api *CachedApi) GetFaculties(structureId int) ([]api2.Faculty, error) {
	var faculties []api2.Faculty
	body := fmt.Sprintf(`{"structureId":%d}`, structureId)

	err := api.makeRequest("POST", "/list/faculties", body, &faculties)
	if err != nil {
		return nil, err
	}

	return faculties, nil
}

// GetCourses returns a list of courses in a faculty
func (api *CachedApi) GetCourses(facultyId int) ([]api2.Course, error) {
	var courses []api2.Course
	body := fmt.Sprintf(`{"facultyId":%d}`, facultyId)

	err := api.makeRequest("POST", "/list/courses", body, &courses)
	if err != nil {
		return nil, err
	}

	return courses, nil
}

// GetGroups returns a list of groups in a faculty
func (api *CachedApi) GetGroups(facultyId int, course int) ([]api2.Group, error) {
	var groups []api2.Group
	body := fmt.Sprintf(`{"facultyId":%d,"course":%d}`, facultyId, course)

	err := api.makeRequest("POST", "/list/groups", body, &groups)
	if err != nil {
		return nil, err
	}

	return groups, nil
}

// GetGroupStudents returns a list of students in a group
func (api *CachedApi) GetGroupStudents(groupId int) ([]api2.Student, error) {
	var students []api2.Student
	body := fmt.Sprintf(`{"groupId":%d}`, groupId)

	err := api.makeRequest("POST", "/list/students-by-group", body, &students)
	if err != nil {
		return nil, err
	}

	return students, nil
}

// GetCallSchedule returns a call schedule
func (api *CachedApi) GetCallSchedule() ([]api2.CallSchedule, error) {
	var callSchedule []api2.CallSchedule

	err := api.makeRequest("POST", "/time-table/call-schedule", "", &callSchedule)
	if err != nil {
		return nil, err
	}

	return callSchedule, nil
}

// GetGroupSchedule returns a schedule for a group
// from dateStart to dateEnd (inclusive)
func (api *CachedApi) GetGroupSchedule(groupId int, dateStart string, dateEnd string) ([]api2.TimeTableDate, error) {
	log.Debugf("Getting schedule for group %d from %s to %s", groupId, dateStart, dateEnd)

	// Get dates range
	start, err := api2.ParseISODate(dateStart)
	if err != nil {
		return nil, err
	}
	end, err := api2.ParseISODate(dateEnd)
	if err != nil {
		return nil, err
	}
	datesRange := int(end.Sub(start).Hours()/24) + 1

	// Get schedule from cache
	rows, err := api.getScheduleStmt.Query(groupId, dateStart, dateEnd)
	if err != nil {
		return nil, err
	}

	defer rows.Close()

	// Check if we need to update the schedule
	var updateNeeded bool

	curTime := time.Now().Unix()
	expires := int64(api.Expires.Seconds())
	count := 0
	schedule := make([]api2.TimeTableDate, datesRange)

	for rows.Next() {
		day := new(CachedDate)
		if err := rows.Scan(&day.GroupId, &day.Date, &day.Lessons, &day.Updated); err != nil {
			return nil, err
		}

		// Check if schedule is outdated
		if curTime-day.Updated > expires {
			updateNeeded = true
		}

		// Add day to schedule
		day2 := new(api2.TimeTableDate)
		if err := json.Unmarshal([]byte(day.Lessons), &day2.Lessons); err != nil {
			return nil, err
		}
		day2.Date = day.Date
		schedule[count] = *day2

		count++
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	if count != datesRange {
		updateNeeded = true
	}

	if !updateNeeded {
		return schedule, nil
	}

	// Update schedule
	log.Debug("Updating schedule")

	// TODO: Use wide range of dates to reduce number of requests
	newSchedule, err := api.api.GetGroupSchedule(groupId, dateStart, dateEnd)
	if err != nil {
		if count == datesRange {
			// Return cached schedule if request failed
			log.Warningf("Error updating schedule: %s", err)
			return schedule, nil
		}
		return nil, err
	}

	tx, err := api.conn.BeginTx(context.Background(), nil)
	if err != nil {
		return nil, err
	}

	stmt, err := tx.PrepareContext(context.Background(), updateScheduleSql)
	if err != nil {
		return nil, err
	}

	// Save schedule to cache
	for _, day := range newSchedule {
		// Convert lessons to JSON string
		lessons, err := json.Marshal(day.Lessons)
		if err != nil {
			return nil, err
		}

		_, err = stmt.Exec(groupId, day.Date, string(lessons), curTime)
		if err != nil {
			return nil, err
		}
	}

	if err := tx.Commit(); err != nil {
		return nil, err
	}

	return newSchedule, nil
}

// GetScheduleExtraInfo returns a extra info for a schedule,
// that can be added by a teacher or university administration.
//
// classCode is a "R1" field from TimeTablePeriod
func (api *CachedApi) GetScheduleExtraInfo(classCode int, date string) (*api2.ScheduleExtraInfo, error) {
	var scheduleExtraInfo api2.ScheduleExtraInfo
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
func (api *CachedApi) GetGroupScheduleDay(groupId int, date string) (*api2.TimeTableDate, error) {
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
