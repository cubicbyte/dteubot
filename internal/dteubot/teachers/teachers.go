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
