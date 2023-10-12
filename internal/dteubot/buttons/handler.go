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
