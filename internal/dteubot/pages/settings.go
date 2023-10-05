package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
)

func CreateSettingsPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	// Mark settings as seen
	if !chatData.SeenSettings {
		chatData.SeenSettings = true
		if err := cm.UpdateChatData(chatData); err != nil {
			return nil, err
		}
	}

	// Get group name
	var groupName string
	if chatData.GroupId == 0 {
		groupName = lang.Text.NotSelected
	} else {
		// TODO: get group name or "Назва невідома (id 741)"
		groupName = format.Formatp(lang.Text.UnknownGroupName, chatData.GroupId)
	}

	// Get classes notification states
	var (
		notif15mNextState string
		notif1mNextState  string
	)
	if chatData.ClassesNotification15m {
		notif15mNextState = "0"
	} else {
		notif15mNextState = "1"
	}
	if chatData.ClassesNotification1m {
		notif1mNextState = "0"
	} else {
		notif1mNextState = "1"
	}

	pageText := format.Formatm(lang.Page.Settings, format.Values{
		"group":    groupName,
		"notif15m": utils.GetSettingIcon(chatData.ClassesNotification15m),
		"notif1m":  utils.GetSettingIcon(chatData.ClassesNotification1m),
	})

	page := Page{
		Text: pageText,
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.SelectGroup, "open.select_group"),
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.SelectLang, "open.select_lang"),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.SettingClNotif15m,
					"set.cl_notif_15m#time=15m&state="+notif15mNextState,
				),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(
					lang.Button.SettingClNotif1m,
					"set.cl_notif_1m#time=1m&state="+notif1mNextState,
				),
			),
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.menu"),
			),
		),
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
