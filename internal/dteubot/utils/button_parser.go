package utils

import "strings"

type ButtonData struct {
	Action string
	Params map[string]string
}

// ParseButtonData parses the telegram button callback Action string.
//
// Params example: "open.schedule.day#date=2023-10-04&day=1"
//
// Returns ButtonData: Action = "open.schedule.day",
// Params = {"date": "2023-10-04", "day": "1"}
func ParseButtonData(buttonData string) *ButtonData {
	if !strings.Contains(buttonData, "#") {
		return &ButtonData{Action: buttonData}
	}

	parsed := strings.Split(buttonData, "#")
	action := parsed[0]

	if len(parsed) == 1 {
		return &ButtonData{Action: action}
	}

	params := make(map[string]string)

	for _, v := range strings.Split(parsed[1], "&") {
		if !strings.Contains(v, "=") {
			params[v] = ""
			continue
		}
		p := strings.SplitN(v, "=", 2)
		params[p[0]] = p[1]
	}

	return &ButtonData{Action: action, Params: params}
}
