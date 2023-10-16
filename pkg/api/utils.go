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
	"time"
)

// FillEmptyDates fills empty dates in given days slice
//
// For example, we have schedule for 2023-08-21 and 2023-08-23.
// If there is no lessons for 2023-08-22, API will return schedule only for 2023-08-21 and 2023-08-23.
// This function will fill empty dates with empty lessons list.
func FillEmptyDates(days *[]TimeTableDate, dateStart string, dateEnd string) error {
	// Get dates difference in days
	date1, err := ParseISODate(dateStart)
	if err != nil {
		return err
	}
	date2, err := ParseISODate(dateEnd)
	if err != nil {
		return err
	}
	delta := int(date2.Sub(date1).Hours() / 24)

	// Fill empty days
	newDates := make([]TimeTableDate, delta+1)
	expectedDate := date1
	expectedDateStr := dateStart

	for i := 0; i <= delta; i++ {
		// Get expected date
		var found = false
		for _, day := range *days {
			if day.Date == expectedDateStr {
				newDates[i] = day
				found = true
				break
			}
		}

		// Add empty day if needed
		if !found {
			newDates[i] = TimeTableDate{
				Date: expectedDateStr,
			}
		}

		// Get next date
		expectedDate = expectedDate.AddDate(0, 0, 1)
		expectedDateStr = expectedDate.Format("2006-01-02")
	}

	*days = newDates

	return nil
}

func getLocation() *time.Location {
	loc, err := time.LoadLocation(Location)
	if err != nil {
		return time.UTC
	}
	return loc
}

// ParseISODate parses ISO date string
func ParseISODate(date string) (time.Time, error) {
	return time.ParseInLocation("2006-01-02", date, getLocation())
}

// GetDateFromDayOfYear returns date from given year and day of year
func GetDateFromDayOfYear(year int, dayOfYear int) time.Time {
	return time.Date(year, 1, 1, 0, 0, 0, 0, getLocation()).AddDate(0, 0, dayOfYear-1)
}

// GetDateRange returns date range from given date and range
//
// For example, we have date 2023-08-21 and range of 10 days.
// Let's convert it to day of year: 233.
// Then we will have 230 and 239 (240 not included) days of year of range.
// So, we will have date range from 2023-08-18 to 2023-08-27.
func GetDateRange(date time.Time, range_ int) (time.Time, time.Time) {
	dayOfYear := date.YearDay()

	// Count dates range
	fromDay := dayOfYear - dayOfYear%range_
	toDay := fromDay + range_ - 1

	// Count years difference
	yearsDiff := toDay / 365
	toDay = toDay % 365

	fromDate := GetDateFromDayOfYear(date.Year(), fromDay)
	toDate := GetDateFromDayOfYear(date.Year()+yearsDiff, toDay)

	return fromDate, toDate
}
