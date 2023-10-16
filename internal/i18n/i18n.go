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
		log.Debugf("Loading language %s", langFile.Name())
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
