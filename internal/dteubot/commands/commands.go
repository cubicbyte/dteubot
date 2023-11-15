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

package commands

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/i18n"
	api2 "github.com/cubicbyte/dteubot/pkg/api"
)

var (
	chatRepo    data.ChatRepository
	userRepo    data.UserRepository
	api         api2.Api
	languages   map[string]i18n.Language
	groupsCache *groupscache.Cache
)

// InitCommands initializes commands package. Must be called before using this package
func InitCommands(
	chatRepo2 data.ChatRepository,
	userRepo2 data.UserRepository,
	api2 api2.Api,
	languages2 map[string]i18n.Language,
	groupsCache2 *groupscache.Cache,
) {
	chatRepo = chatRepo2
	userRepo = userRepo2
	api = api2
	languages = languages2
	groupsCache = groupsCache2
}
