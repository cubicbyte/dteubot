package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

func CreateCoursesListPage(cm *data.ChatDataManager, facultyId int, structureId int) (*Page, error) {
	lang, err := utils.GetLang(cm)
	if err != nil {
		return nil, err
	}

	courses, err := settings.Api.GetCourses(facultyId)
	if err != nil {
		return nil, err
	}

	buttons := make([][]tgbotapi.InlineKeyboardButton, len(courses)+1)
	backBtnQuery := "open.select_faculty#structureId=" + strconv.Itoa(structureId)
	buttons[0] = tgbotapi.NewInlineKeyboardRow(
		tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backBtnQuery),
	)

	for i, course := range courses {
		query := "select.schedule.course#course=" + strconv.Itoa(course.Course) +
			"&facultyId=" + strconv.Itoa(facultyId) +
			"&structureId=" + strconv.Itoa(structureId)
		buttons[i+1] = tgbotapi.NewInlineKeyboardRow(
			tgbotapi.NewInlineKeyboardButtonData(strconv.Itoa(course.Course), query),
		)
	}

	page := Page{
		Text:           lang.Page.CourseSelection,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
