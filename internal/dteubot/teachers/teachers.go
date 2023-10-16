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

package teachers

import (
	"encoding/csv"
	"github.com/op/go-logging"
	"io"
	"os"
	"strings"
)

var log = logging.MustGetLogger("teachers")

// TeachersList is a struct for getting teacher profile links
type TeachersList struct {
	File     string
	teachers map[string]string
}

// Load loads teachers list from csv file: name;page_link
func (t *TeachersList) Load() error {
	log.Info("Loading teachers list")

	t.teachers = make(map[string]string)

	// Open file
	f, err := os.Open(t.File)
	if err != nil {
		return err
	}

	// Read file
	reader := csv.NewReader(f)
	reader.Comma = ';'
	reader.FieldsPerRecord = 2

	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}

		name := convertName(record[0])
		t.teachers[name] = record[1]
	}

	return f.Close()
}

// GetLink returns teacher profile link by name
func (t *TeachersList) GetLink(name string) (string, bool) {
	name = convertName(name)
	link, ok := t.teachers[name]
	return link, ok
}

// convertName converts teacher name to hashable string.
// Sometimes teacher name have some extra spaces, other symbols, etc.
func convertName(name string) string {
	// To lower
	name = strings.ToLower(name)

	// Remove extra spaces
	name = strings.Trim(name, " \n")
	name = strings.ReplaceAll(name, "  ", " ")

	// Replace latin letters to cyrillic
	replacer := strings.NewReplacer(
		"e", "е",
		"i", "і",
		"o", "о",
		"p", "р",
		"a", "а",
		"x", "х",
		"c", "с",
	)

	name = replacer.Replace(name)

	return name
}
