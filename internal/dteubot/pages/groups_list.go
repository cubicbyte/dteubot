package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"strconv"
)

const rowSize = 3

func CreateGroupsListPage(cm *data.ChatDataManager, facultyId int, course int, structureId int) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	groups, err := settings.Api.GetGroups(facultyId, course)
	if err != nil {
		return nil, err
	}

	// Create back button
	rowsCount := len(groups)/rowSize + 1
	if len(groups)%rowSize != 0 {
		rowsCount++
	}
	buttons := make([][]tgbotapi.InlineKeyboardButton, rowsCount)
	backBtnQuery := "open.select_faculty#facultyId=" + strconv.Itoa(facultyId) +
		"#structureId=" + strconv.Itoa(structureId)
	buttons[0] = tgbotapi.NewInlineKeyboardRow(
		tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, backBtnQuery),
	)

	// Create group buttons
	lastRow := make([]tgbotapi.InlineKeyboardButton, min(rowSize, len(groups)))
	for i, group := range groups {
		query := "select.schedule.group#groupId=" + strconv.Itoa(group.Id)
		lastRow[i%rowSize] = tgbotapi.NewInlineKeyboardButtonData(group.Name, query)
		if i%rowSize == rowSize-1 {
			buttons[i/rowSize+1] = lastRow
			lastRow = make([]tgbotapi.InlineKeyboardButton, min(rowSize, len(groups)-i-1))
		}
	}
	if len(lastRow) > 0 {
		buttons[len(buttons)-1] = lastRow
	}

	page := Page{
		Text:           lang.Page.GroupSelection,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(buttons...),
		ParseMode:      "MarkdownV2",
	}

	return &page, nil
}
