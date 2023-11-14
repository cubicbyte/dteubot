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

// What it does?
//   Provides cache for groups to get group name by id
// Why it's needed?
//   Because API doesn't provide any way to get group name by id, but
//   we need to show it for example in settings menu

package groupscache

import (
	"encoding/csv"
	"github.com/cubicbyte/dteubot/pkg/api"
	"github.com/op/go-logging"
	"io"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

var log = logging.MustGetLogger("GroupsCache")

// TTL is time to live for group in cache
const TTL = 60 * 60 * 24 // 1 day

// Group represents group
type Group struct {
	Id        int
	Name      string
	Course    int
	FacultyId int
	Updated   int64
}

// Cache provides cache for groups
type Cache struct {
	File   string
	groups map[int]Group
	api    api.IApi
	mu     sync.Mutex
}

// New creates new cache instance
func New(file string, api2 api.IApi) *Cache {
	return &Cache{
		File:   file,
		groups: make(map[int]Group),
		api:    api2,
		mu:     sync.Mutex{},
	}
}

// AddGroups adds groups to cache
func (c *Cache) AddGroups(groups []Group) error {
	for _, group := range groups {
		c.groups[group.Id] = group
	}

	return c.Save()
}

// AddGroup adds group to cache
func (c *Cache) AddGroup(group Group) error {
	c.groups[group.Id] = group

	return c.Save()
}

// GetGroupById returns group by id
func (c *Cache) GetGroupById(id int) (*Group, error) {
	log.Debugf("Getting group %d\n", id)

	group, ok := c.groups[id]
	if !ok {
		return nil, nil
	}

	// Check if group is outdated
	timestamp := time.Now().Unix()
	if timestamp-group.Updated > TTL {
		// Update group
		newGroup, err := c.updateGroup(group)
		if err != nil {
			if ok {
				// Return old group if update failed
				return &group, err
			}
			return nil, err
		}

		return newGroup, nil
	}

	return &group, nil
}

// GetGroupByName returns group by name. Not case sensitive
func (c *Cache) GetGroupByName(name string) (*Group, error) {
	log.Debugf("Getting group %s\n", name)

	name = strings.ToLower(name)

	for _, group := range c.groups {
		groupName := strings.ToLower(group.Name)

		if groupName == name {
			// Check if group is outdated
			timestamp := time.Now().Unix()
			if timestamp-group.Updated > TTL {
				// Update group
				newGroup, err := c.updateGroup(group)
				if err != nil {
					return nil, err
				}

				return newGroup, nil
			}

			return &group, nil
		}
	}

	return nil, nil
}

// GetGroups returns all groups
func (c *Cache) updateGroup(group Group) (*Group, error) {
	log.Debugf("Updating group %d\n", group.Id)

	// Get group from api at current course
	groups, err := c.api.GetGroups(group.FacultyId, group.Course)
	if err != nil {
		return nil, err
	}

	for _, g := range groups {
		if g.Id == group.Id {
			// Update group
			group.Name = g.Name
			group.Updated = time.Now().Unix()

			// Save cache
			err := c.Save()
			if err != nil {
				return nil, err
			}

			return &group, nil
		}
	}

	// Group not found. Try to find group at next courses
	courses, err := c.api.GetCourses(group.FacultyId)
	if err != nil {
		return nil, err
	}

	for _, course := range courses {
		if course.Course <= group.Course {
			continue
		}

		groups, err := c.api.GetGroups(group.FacultyId, course.Course)
		if err != nil {
			return nil, err
		}

		for _, g := range groups {
			if g.Id == group.Id {
				// Update group
				group.Name = g.Name
				group.Course = course.Course
				group.Updated = time.Now().Unix()

				// Save cache
				err := c.Save()
				if err != nil {
					return nil, err
				}

				return &group, nil
			}
		}
	}

	// Group not found at all courses
	return nil, nil
}

// Load cache from csv file
//
// File format:
//
//	id;name;course;faculty_id;updated
func (c *Cache) Load() error {
	log.Infof("Loading groups cache from %s\n", c.File)

	// Open csv file
	f, err := os.OpenFile(c.File, os.O_RDWR|os.O_CREATE, 0666)
	if err != nil {
		return err
	}

	defer f.Close()

	// Read file
	reader := csv.NewReader(f)
	reader.Comma = ';'

	// Read all records
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			if err := f.Close(); err != nil {
				return err
			}
			return err
		}

		// Parse group
		id, err := strconv.Atoi(record[0])
		if err != nil {
			return err
		}
		course, err := strconv.Atoi(record[2])
		if err != nil {
			return err
		}
		facultyId, err := strconv.Atoi(record[3])
		if err != nil {
			return err
		}
		updated, err := strconv.ParseInt(record[4], 10, 64)
		if err != nil {
			return err
		}

		group := Group{
			Id:        id,
			Name:      record[1],
			Course:    course,
			FacultyId: facultyId,
			Updated:   updated,
		}

		c.groups[id] = group
	}

	return nil
}

// Save cache to csv file
func (c *Cache) Save() error {
	log.Debugf("Saving groups cache to %s\n", c.File)

	// Lock mutex
	c.mu.Lock()
	defer c.mu.Unlock()

	// Open csv file
	f, err := os.OpenFile(c.File, os.O_RDWR|os.O_CREATE, 0666)
	if err != nil {
		return err
	}

	defer f.Close()

	// Create csv writer
	writer := csv.NewWriter(f)
	writer.Comma = ';'

	// Write all groups
	for _, group := range c.groups {
		err := writer.Write([]string{
			strconv.Itoa(group.Id),
			group.Name,
			strconv.Itoa(group.Course),
			strconv.Itoa(group.FacultyId),
			strconv.FormatInt(group.Updated, 10),
		})
		if err != nil {
			return err
		}
	}

	// Flush csv writer
	writer.Flush()

	if err := writer.Error(); err != nil {
		return err
	}

	return nil
}
