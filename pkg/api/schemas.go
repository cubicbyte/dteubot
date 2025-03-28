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

type Structure struct {
	Id        int    `json:"id"`
	ShortName string `json:"shortName"`
	FullName  string `json:"fullName"`
}

type Faculty struct {
	Id        int    `json:"id"`
	ShortName string `json:"shortName"`
	FullName  string `json:"fullName"`
}

type Course struct {
	Course int `json:"course"`
}

type Group struct {
	Id            int    `json:"id"`
	Name          string `json:"name"`
	Course        int    `json:"course"`
	Priority      int    `json:"priority"`
	EducationForm int    `json:"educationForm"`
}

type Student struct {
	Id         int    `json:"id"`
	FirstName  string `json:"firstName"`
	SecondName string `json:"secondName"`
	LastName   string `json:"lastName"`
}

type CallScheduleEntry struct {
	TimeStart string `json:"timeStart"`
	TimeEnd   string `json:"timeEnd"`
	Number    int    `json:"number"`
	Length    int    `json:"length"`
}

type TimeTablePeriod struct {
	R1           int `json:"r1"`
	Rz14         int `json:"rz14"`
	Rz15         int `json:"rz15"`
	R5           int `json:"r5"`
	DisciplineId int `json:"disciplineId"`
	// Disabled because it can sometimes be bool instead of int,
	// which causes errors. University's fault.
	//EducationDisciplineId int    `json:"educationDisciplineId"`
	DisciplineFullName  string `json:"disciplineFullName"`
	DisciplineShortName string `json:"disciplineShortName"`
	Classroom           string `json:"classroom"`
	TimeStart           string `json:"timeStart"`
	TimeEnd             string `json:"timeEnd"`
	TeachersName        string `json:"teachersName"`
	TeachersNameFull    string `json:"teachersNameFull"`
	Type                int    `json:"type"`
	TypeStr             string `json:"typeStr"`
	DateUpdated         string `json:"dateUpdated"`
	NonstandardTime     bool   `json:"nonstandardTime"`
	Groups              string `json:"groups"`
	ChairName           string `json:"chairName"`
	ExtraText           bool   `json:"extraText"`
	LessonYear          int    `json:"lessonYear"`
	Semester            int    `json:"semester"`
}

type TimeTableLesson struct {
	Number  int               `json:"number"`
	Periods []TimeTablePeriod `json:"periods"`
}

type TimeTableDate struct {
	Date    string            `json:"date"`
	Lessons []TimeTableLesson `json:"lessons"`
}

type ScheduleExtraInfo struct {
	Html string `json:"html"`
}

type CallSchedule []CallScheduleEntry
type Schedule []TimeTableDate

func (stud *Student) GetFullName() string {
	return stud.LastName + " " + stud.FirstName + " " + stud.SecondName
}

func (s *CallSchedule) GetCall(number int) *CallScheduleEntry {
	for _, call := range *s {
		if call.Number == number {
			return &call
		}
	}
	return nil
}

func (s *Schedule) GetDay(date string) *TimeTableDate {
	for _, day := range *s {
		if day.Date == date {
			return &day
		}
	}
	return nil
}

// GetLesson returns a lesson with a specific number from a day.
func (day *TimeTableDate) GetLesson(number int) *TimeTableLesson {
	for _, lesson := range day.Lessons {
		if lesson.Number == number {
			return &lesson
		}
	}
	return nil
}

type Chair struct {
	Id        int    `json:"id"`
	ShortName string `json:"shortName"`
	FullName  string `json:"fullName"`
}

type Person struct {
	Id         int    `json:"id"`
	FirstName  string `json:"firstName"`
	SecondName string `json:"secondName"`
	LastName   string `json:"lastName"`
}

func (p *Person) GetFullName() string {
	return p.LastName + " " + p.FirstName + " " + p.SecondName
}
