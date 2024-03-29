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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"time"
)

func HandleScheduleDayButton(bot *gotgbot.Bot, ctx *ext.Context) error {
	// Get chat
	chat, err := chatRepo.GetById(ctx.EffectiveChat.Id)
	if err != nil {
		return err
	}

	lang, err := utils.GetLang(chat.LanguageCode, languages)
	if err != nil {
		return err
	}

	// Get date from button params
	button := utils.ParseButtonData(ctx.CallbackQuery.Data)

	date, ok := button.Params["date"]
	if !ok {
		return errors.New("date param not found")
	}

	// Open schedule page
	page, err := pages.CreateSchedulePage(lang, chat.GroupId, date)
	err = openPage(bot, ctx, page, err)
	if err != nil {
		return err
	}

	// Suggest notifications
	if err := SuggestNotifications(chat, lang, bot); err != nil {
		return err
	}

	return nil
}

func SuggestNotifications(chat *data.Chat, lang i18n.Language, bot *gotgbot.Bot) error {
	if chat.SeenSettings {
		return nil
	}

	// Update chat
	chat.SeenSettings = true

	if err := chatRepo.Update(chat); err != nil {
		return err
	}

	// Wait for 1 second
	time.Sleep(1 * time.Second)

	// Send notifications feature suggestion page
	page, err := pages.CreateNotificationFeatureSuggestionPage(lang)
	if err != nil {
		return err
	}

	opts := page.CreateSendMessageOpts()
	_, err = bot.SendMessage(chat.Id, page.Text, &opts)
	if err != nil {
		return err
	}

	return nil
}
