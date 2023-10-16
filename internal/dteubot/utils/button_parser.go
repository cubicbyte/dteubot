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
