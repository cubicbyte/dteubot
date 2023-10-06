package logging

import (
	"github.com/op/go-logging"
	"os"
)

var fileFormat = logging.MustStringFormatter(
	`%{time:2006-01-02 15:04:05.000} %{module} %{level}: %{message}`,
)

var cmdFormat = logging.MustStringFormatter(
	`%{color}%{time:15:04:05.000} %{module} %{level} ▶%{color:reset} %{message}`,
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
