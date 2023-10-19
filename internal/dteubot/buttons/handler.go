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
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("bot")

func HandleButton(u *tgbotapi.Update) error {
	log.Infof("Handling button %s from %d\n", u.CallbackQuery.Data, u.CallbackQuery.From.ID)

	button := utils.ParseButtonData(u.CallbackQuery.Data)

	switch button.Action {
	case "open.menu":
		if err := HandleMenuButton(u); err != nil {
			return err
		}
	case "open.settings":
		if err := HandleSettingsButton(u); err != nil {
			return err
		}
	case "open.calls":
		if err := HandleCallsButton(u); err != nil {
			return err
		}
	case "open.more":
		if err := HandleMoreButton(u); err != nil {
			return err
		}
	case "open.admin_panel":
		if err := HandleAdminPanelButton(u); err != nil {
			return err
		}
	case "open.schedule.today":
		if err := HandleScheduleTodayButton(u); err != nil {
			return err
		}
	case "open.schedule.extra":
		if err := HandleScheduleExtraButton(u); err != nil {
			return err
		}
	case "open.info":
		if err := HandleInfoButton(u); err != nil {
			return err
		}
	case "open.left":
		if err := HandleLeftButton(u); err != nil {
			return err
		}
	case "open.students_list":
		if err := HandleStudentsListButton(u); err != nil {
			return err
		}
	case "open.select_group":
		if err := HandleOpenSelectGroupButton(u); err != nil {
			return err
		}
	case "open.select_lang":
		if err := HandleOpenSelectLanguageButton(u); err != nil {
			return err
		}
	case "open.schedule.day":
		if err := HandleScheduleDayButton(u); err != nil {
			return err
		}
	case "select.schedule.structure":
		if err := HandleSelectStructureButton(u); err != nil {
			return err
		}
	case "select.schedule.faculty":
		if err := HandleSelectFacultyButton(u); err != nil {
			return err
		}
	case "select.schedule.course":
		if err := HandleSelectCourseButton(u); err != nil {
			return err
		}
	case "select.schedule.group":
		if err := HandleSelectGroupButton(u); err != nil {
			return err
		}
	case "select.lang":
		if err := HandleSelectLanguageButton(u); err != nil {
			return err
		}
	case "set.cl_notif":
		if err := HandleSetClassesNotificationsButton(u); err != nil {
			return err
		}
	case "set.cl_notif_next_part":
		if err := HandleSetClassesNotificationsNextPartButton(u); err != nil {
			return err
		}
	case "admin.clear_cache":
		if err := HandleClearCacheButton(u); err != nil {
			return err
		}
	case "admin.clear_logs":
		if err := HandleClearLogsButton(u); err != nil {
			return err
		}
	case "admin.get_logs":
		if err := HandleSendLogsButton(u); err != nil {
			return err
		}
	default:
		log.Warningf("Unknown button action: %s\n", button.Action)
		if err := HandleUnsupportedButton(u); err != nil {
			return err
		}
	}

	return nil
}

func EditMessageRequest(page *pages.Page, cb *tgbotapi.CallbackQuery) tgbotapi.EditMessageTextConfig {
	return page.CreateEditMessage(cb.Message.Chat.ID, cb.Message.MessageID)
}

func checkAdmin(u *tgbotapi.Update) (bool, error) {
	manager := utils.GetUserDataManager(u.CallbackQuery.From.ID)

	userData, err := manager.GetUserData()
	if err != nil {
		return false, err
	}

	return userData.IsAdmin, nil
}
