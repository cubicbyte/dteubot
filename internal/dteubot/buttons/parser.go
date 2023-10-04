package buttons

import "strings"

type ButtonData struct {
	query string
	data  map[string]string
}

// ParseButtonData parses the telegram button callback query string.
//
// Query example: "open.schedule.day#date=2023-10-04&day=1"
//
// Returns ButtonData: query = "open.schedule.day",
// data = {"date": "2023-10-04", "day": "1"}
func ParseButtonData(callbackQuery string) *ButtonData {
	if !strings.Contains(callbackQuery, "#") {
		return &ButtonData{query: callbackQuery}
	}

	parsed := strings.Split(callbackQuery, "#")
	query := parsed[0]
	data := make(map[string]string)

	for _, v := range strings.Split(parsed[1], "&") {
		p := strings.Split(v, "=")
		data[p[0]] = p[1]
	}

	return &ButtonData{query: query, data: data}
}
