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

package logging

import (
	"github.com/op/go-logging"
	"os"
)

var fileFormat = logging.MustStringFormatter(
	`%{time:2006-01-02 15:04:05.000} %{level} %{module}: %{message}`,
)

var cmdFormat = logging.MustStringFormatter(
	`%{color}%{time:15:04:05.000} %{level} %{module} ▶%{color:reset} %{message}`,
)

const LogFilePath = "debug.log"

var LogFile *os.File

// Init initializes logging system
func Init() error {
	logLevel := os.Getenv("LOG_LEVEL")
	if logLevel == "" {
		logLevel = "INFO"
	}

	// Disable logging if needed
	if logLevel == "DISABLED" {
		backend := logging.NewLogBackend(os.Stderr, "", 0)
		backendLeveled := logging.AddModuleLevel(backend)
		backendLeveled.SetLevel(logging.CRITICAL, "")
		logging.SetBackend(backendLeveled)
		return nil
	}

	// Open log file
	var err error
	LogFile, err = os.OpenFile(LogFilePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}

	// Create file and cmd loggers
	fsBackend := logging.NewLogBackend(LogFile, "", 0)
	fsBackendFormatter := logging.NewBackendFormatter(fsBackend, fileFormat)
	fsBackendLeveled := logging.AddModuleLevel(fsBackendFormatter)

	cmdBackend := logging.NewLogBackend(os.Stderr, "", 0)
	cmdBackendFormatter := logging.NewBackendFormatter(cmdBackend, cmdFormat)
	cmdBackendLeveled := logging.AddModuleLevel(cmdBackendFormatter)

	// Set log level
	switch logLevel {
	case "DEBUG":
		fsBackendLeveled.SetLevel(logging.DEBUG, "")
		cmdBackendLeveled.SetLevel(logging.DEBUG, "")
	case "INFO":
		fsBackendLeveled.SetLevel(logging.INFO, "")
		cmdBackendLeveled.SetLevel(logging.INFO, "")
	case "WARNING":
		fsBackendLeveled.SetLevel(logging.WARNING, "")
		cmdBackendLeveled.SetLevel(logging.WARNING, "")
	case "ERROR":
		fsBackendLeveled.SetLevel(logging.ERROR, "")
		cmdBackendLeveled.SetLevel(logging.ERROR, "")
	case "CRITICAL":
		fsBackendLeveled.SetLevel(logging.CRITICAL, "")
		cmdBackendLeveled.SetLevel(logging.CRITICAL, "")
	}

	logging.SetBackend(fsBackendLeveled, cmdBackendLeveled)

	return nil
}
