package i18n

import (
	"embed"
	"github.com/op/go-logging"
	"gopkg.in/yaml.v3"
)

//go:embed langs/*.yaml
var langsFS embed.FS

var log = logging.MustGetLogger("i18n")

// LoadLangs loads all languages from given path.
// All language files should have .yaml extension and be in langs/ directory
func LoadLangs() (map[string]Language, error) {
	log.Info("Loading languages")

	obj := make(map[string]Language)

	// Get all lang files
	langFiles, err := langsFS.ReadDir("langs")
	if err != nil {
		return nil, err
	}

	// Load all lang files
	for _, langFile := range langFiles {
		lang, err := loadLang("langs/" + langFile.Name())
		if err != nil {
			return nil, err
		}
		fileName := langFile.Name()[0 : len(langFile.Name())-5]
		obj[fileName] = *lang
	}

	return obj, nil
}

// loadLang loads language from given path.
func loadLang(path string) (*Language, error) {
	// Read file
	f, err := langsFS.Open(path)
	if err != nil {
		return nil, err
	}

	// Parse file
	lang := new(Language)
	err = yaml.NewDecoder(f).Decode(lang)
	if err != nil {
		return nil, err
	}

	return lang, nil
}
