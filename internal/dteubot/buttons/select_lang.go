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
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/groupscache"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleSelectLanguageButton(u *tgbotapi.Update, bot *tgbotapi.BotAPI, lang *i18n.Language, langs map[string]i18n.Language, chat *data.Chat, chatRepo data.ChatRepository, groups *groupscache.Cache) error {
	button := utils.ParseButtonData(u.CallbackQuery.Data)

	// Get language code from button params
	langCode, ok := button.Params["lang"]
	if !ok {
		return errors.New("lang param not found")
	}

	// Go back to settings if user selected the same language
	if langCode == chat.LanguageCode {
		page, err := pages.CreateSettingsPage(lang, chat, chatRepo, groups)
		return editPage(page, err, u, bot)
	}

	// Update chat language
	chat.LanguageCode = langCode

	err := chatRepo.Update(chat)
	if err != nil {
		return err
	}

	// Get new language
	lang, err = utils.GetLang(langCode, langs)
	if err != nil {
		return err
	}

	// Update page
	page, err := pages.CreateLanguageSelectionPage(lang, langs, "open.settings#from=select_lang")
	return editPage(page, err, u, bot)
}
