package pages

import (
	"github.com/cubicbyte/dteubot/internal/data"
)

func CreateGreetingPage(cm *data.ChatDataManager) (*Page, error) {
	lang, err := cm.GetLanguage()
	if err != nil {
		return nil, err
	}

	page := Page{
		Text:      lang.Page.Greeting,
		ParseMode: "MarkdownV2",
	}

	return &page, nil
}
