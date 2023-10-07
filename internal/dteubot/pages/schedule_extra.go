package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/dlclark/regexp2"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/sirkon/go-format/v2"
	"strconv"
	"strings"
)

var telegramSupportedHTMLTags = [...]string{
	"a", "s", "i", "b", "u", "em", "pre",
	"ins", "del", "code", "strong", "strike",
}

func CreateScheduleExtraInfoPage(cm *data.ChatDataManager, date string) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	chatData, err := cm.GetChatData()
	if err != nil {
		return nil, err
	}

	schedule, err := settings.Api.GetGroupScheduleDay(chatData.GroupId, date)
	if err != nil {
		return nil, err
	}

	pageText := ""
	for _, lesson := range schedule.Lessons {
		for _, period := range lesson.Periods {
			if !period.ExtraText {
				continue
			}

			// Get extra info
			extraText, err := settings.Api.GetScheduleExtraInfo(period.R1, date)
			if err != nil {
				return nil, err
			}

			// Clean HTML from unsupported tags
			extraTextStr, err := cleanHTML(extraText.Html)
			if err != nil {
				return nil, err
			}

			// Remove all spaces and newlines from the beginning and end of the string
			extraTextStr = strings.Trim(extraTextStr, "\n ")

			pageText += "<b>" + strconv.Itoa(lesson.Number) + ")</b> " + extraTextStr + "\n\n"
		}
	}

	page := Page{
		Text: format.Formatp(lang.Page.ScheduleExtraInfo, pageText),
		InlineKeyboard: tgbotapi.NewInlineKeyboardMarkup(
			tgbotapi.NewInlineKeyboardRow(
				tgbotapi.NewInlineKeyboardButtonData(lang.Button.Back, "open.schedule.day#date="+date),
			),
		),
		ParseMode:             "HTML",
		DisableWebPagePreview: true,
	}

	return &page, nil
}

func cleanHTML(text string) (string, error) {
	// Save line breaks
	text = strings.ReplaceAll(text, "<br>", "\n")
	text = strings.ReplaceAll(text, "<br/>", "\n")
	text = strings.ReplaceAll(text, "<br />", "\n")

	// Remove all other tags
	// tag|tag2|tag3
	supported := strings.Join(telegramSupportedHTMLTags[:], "|")
	cleanr, err := regexp2.Compile("<(?!\\/?("+supported+")\\b)[^>]*>", regexp2.IgnoreCase)
	if err != nil {
		return "", err
	}

	text, err = cleanr.Replace(text, "", -1, -1)
	if err != nil {
		return "", err
	}

	return text, nil
}
