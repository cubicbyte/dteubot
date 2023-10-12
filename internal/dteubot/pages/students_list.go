package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
	"strconv"
)

func CreateStudentsListPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	students, err := settings.Api.GetGroupStudents(chatData.GroupId)
	if err != nil {
		return nil, err
	}

	// Get group name
	var groupName string
	if chatData.GroupId == -1 {
		groupName = lang.Text.NotSelected
	} else {
		group, err := settings.GroupsCache.GetGroup(chatData.GroupId)
		if err != nil {
			return nil, err
		}
		if group == nil {
			groupId := utils.EscapeTelegramMarkdownV2(strconv.Itoa(chatData.GroupId))
			groupName = format.Formatp(lang.Text.UnknownGroupName, groupId)
		} else {
			groupName = utils.EscapeTelegramMarkdownV2(group.Name)
		}
	}

	pageText := ""
	for i, student := range students {
		studentPos := strconv.Itoa(i + 1)
		name := ""
		name += utils.EscapeTelegramMarkdownV2(student.LastName) + " "
		name += utils.EscapeTelegramMarkdownV2(student.FirstName) + " "
		name += utils.EscapeTelegramMarkdownV2(student.SecondName)

		pageText += "*" + studentPos + "*\\) " + name + "\n"
	}

	pageText = format.Formatm(lang.Page.StudentsList, format.Values{
		"group":    groupName,
		"students": pageText,
	})

	page := Page{
		Text: pageText,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.more"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
