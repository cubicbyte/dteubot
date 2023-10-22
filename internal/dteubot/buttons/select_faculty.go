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

package buttons

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func HandleSelectFacultyButton(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, api2 api.IApi) error {
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	// Get faculty id and structure id from button params
	facultyId, ok := button.Params["facultyId"]
	if !ok {
		return errors.New("facultyId param not found")
	}
	structureId, ok := button.Params["structureId"]
	if !ok {
		return errors.New("structureId param not found")
	}

	facId, err := strconv.Atoi(facultyId)
	if err != nil {
		return err
	}
	structId, err := strconv.Atoi(structureId)
	if err != nil {
		return err
	}

	// Open courses list page
	page, err := pages.CreateCoursesListPage(lang, facId, structId, api2)
	return editPage(page, err, u, bot)
}
