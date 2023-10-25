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

package dteubot

import (
	"errors"
	"github.com/cubicbyte/dteubot/internal/dteubot/buttons"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

func HandleButtonClick(u *tgbotapi.Update) error {
	log.Infof("Handling button %s from %d\n", u.CallbackQuery.Data, u.CallbackQuery.From.ID)

	chat, err := chatRepo.GetById(u.CallbackQuery.Message.Chat.ID)
	if err != nil {
		return err
	}
	if chat == nil {
		return errors.New("chat not found")
	}

	user, err := userRepo.GetById(u.CallbackQuery.From.ID)
	if err != nil {
		return err
	}
	if user == nil {
		return errors.New("user not found")
	}

	lang, err := utils.GetLang(chat.LanguageCode, languages)
	if err != nil {
		return err
	}

	button := utils.ParseButtonData(u.CallbackQuery.Data)

	switch button.Action {
	case "open.menu":
		return buttons.HandleMenuButton(u, bot, lang, user)
	case "open.settings":
		return buttons.HandleSettingsButton(u, bot, lang, chat, chatRepo, groupsCache)
	case "open.calls":
		return buttons.HandleCallsButton(u, bot, lang, api)
	case "open.more":
		return buttons.HandleMoreButton(u, bot, lang)
	case "open.admin_panel":
		return buttons.HandleAdminPanelButton(u, bot, lang, user)
	case "open.schedule.today":
		return buttons.HandleScheduleTodayButton(u, bot, lang, chat, api, teachersList)
	case "open.schedule.extra":
		return buttons.HandleScheduleExtraButton(u, bot, lang, chat.GroupId, api)
	case "open.info":
		return buttons.HandleInfoButton(u, bot, lang)
	case "open.left":
		return buttons.HandleLeftButton(u, bot, lang, chat.GroupId, api)
	case "open.students_list":
		return buttons.HandleStudentsListButton(u, bot, lang, chat.GroupId, groupsCache, api)
	case "open.select_group":
		return buttons.HandleOpenSelectGroupButton(u, bot, lang, api)
	case "open.select_lang":
		return buttons.HandleOpenSelectLanguageButton(u, bot, lang, languages)
	case "open.schedule.day":
		return buttons.HandleScheduleDayButton(u, bot, lang, chat.GroupId, api, teachersList)
	case "select.schedule.structure":
		return buttons.HandleSelectStructureButton(u, bot, lang, api)
	case "select.schedule.faculty":
		return buttons.HandleSelectFacultyButton(u, bot, lang, api)
	case "select.schedule.course":
		return buttons.HandleSelectCourseButton(u, bot, lang, api, groupsCache)
	case "select.schedule.group":
		return buttons.HandleSelectGroupButton(u, bot, lang, chat, user, chatRepo)
	case "select.lang":
		return buttons.HandleSelectLanguageButton(u, bot, lang, languages, chat, chatRepo, groupsCache)
	case "set.cl_notif":
		return buttons.HandleSetClassesNotificationsButton(u, bot, lang, chat, chatRepo, groupsCache)
	case "set.cl_notif_next_part":
		return buttons.HandleSetClassesNotificationsNextPartButton(u, bot, lang, chat, chatRepo, groupsCache)
	case "admin.clear_cache":
		return buttons.HandleClearCacheButton(u, bot, lang, user)
	case "admin.clear_logs":
		return buttons.HandleClearLogsButton(u, bot, lang, user)
	case "admin.get_logs":
		return buttons.HandleSendLogsButton(u, bot, lang, user)
	default:
		log.Warningf("Unknown button action: %s\n", button.Action)
		return buttons.HandleUnsupportedButton(u, bot, lang, user)
	}
}
