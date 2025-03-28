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
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"strconv"
)

func HandleSelectTeacherButton(bot *gotgbot.Bot, ctx *ext.Context) error {
	// Get chat and user
	chat, err := chatRepo.GetById(ctx.EffectiveChat.Id)
	if err != nil {
		return err
	}

	user, err := userRepo.GetById(ctx.EffectiveUser.Id)
	if err != nil {
		return err
	}

	lang, err := utils.GetLang(chat.LanguageCode, languages)
	if err != nil {
		return err
	}

	// Get group id from button params
	button := utils.ParseButtonData(ctx.CallbackQuery.Data)

	idStr, ok := button.Params["id"]
	if !ok {
		return errors.New("id param not found")
	}

	teacherId, err := strconv.Atoi(idStr)
	if err != nil {
		return err
	}

	// Update chat group id
	chat.TeacherId = teacherId

	err = chatRepo.Update(chat)
	if err != nil {
		return err
	}

	// Open menu page
	page, err := pages.CreateMenuPage(lang, user)
	return openPage(bot, ctx, page, err)
}
