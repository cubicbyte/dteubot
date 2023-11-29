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

package main

import (
	"fmt"
	"github.com/cubicbyte/dteubot/internal/config"
	"github.com/cubicbyte/dteubot/internal/dteubot"
	"github.com/cubicbyte/dteubot/internal/logging"
	"os"
	// Fixes "Unknown time zone" error. https://github.com/golang/go/issues/55899
	// Will increase binary size by ~550KB
	_ "time/tzdata"
)

func main() {
	// Load .env file
	if err := config.LoadEnv(); err != nil {
		fmt.Printf("Error loading .env file: %s\n", err)
		os.Exit(1)
	}

	// Validate environment variables (config)
	if err := config.ValidateEnv(); err != nil {
		fmt.Printf("Error validating .env file: %s\n", err)
		os.Exit(1)
	}

	// Initialize logging
	if err := logging.Init(); err != nil {
		fmt.Printf("Error initializing logging: %s\n", err)
		os.Exit(1)
	}

	dteubot.Setup()
	dteubot.Run()
}
