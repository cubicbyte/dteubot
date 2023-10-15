package errorhandler

import (
	"errors"
	"fmt"
	"github.com/cubicbyte/dteubot/internal/dteubot/buttons"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/settings"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/pkg/api"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/op/go-logging"
	"github.com/sirkon/go-format/v2"
	"net/http"
	"net/url"
	"os"
	"strings"
)

var log = logging.MustGetLogger("ErrorHandler")

func HandleError(err error, update tgbotapi.Update) {
	var urlError *url.Error
	var httpApiError *api.HTTPApiError
	var tgError *tgbotapi.Error

	switch {
	case errors.As(err, &urlError):
		// Can't make request to the university API

		chat := update.FromChat()
		if chat == nil {
			// Api error with no chat
			log.Errorf("Api request error with no chat: %s", err)
			SendErrorToTelegram(err)
			break
		}

		cm := utils.GetChatDataManager(chat.ID)
		page, err := pages.CreateApiUnavailablePage(cm)
		if err != nil {
			log.Errorf("Error creating api unavailable page: %s", err)
			SendErrorToTelegram(err)
			break
		}

		if update.CallbackQuery != nil {
			_, err = settings.Bot.Send(buttons.EditMessageRequest(page, update.CallbackQuery))
		} else {
			_, err = settings.Bot.Send(page.CreateMessage(cm.ChatId))
		}

		if err != nil {
			log.Errorf("Error sending api unavailable page: %s", err)
			SendErrorToTelegram(err)
		}
	case errors.As(err, &httpApiError):
		// Non-200 api status code

		chat := update.FromChat()
		if chat == nil {
			// Api error with no chat
			log.Errorf("Api error with no chat: %s", err)
			SendErrorToTelegram(err)
			break
		}

		log.Warningf("Api %d error: %s", httpApiError.Code, httpApiError.Body)

		cm := utils.GetChatDataManager(chat.ID)

		var page *pages.Page
		var pageErr error

		switch httpApiError.Code {
		case http.StatusUnauthorized:
			page, pageErr = pages.CreateForbiddenPage(cm, "open.menu#from=unauthorized")

		case http.StatusInternalServerError:
			page, pageErr = pages.CreateApiUnavailablePage(cm)

		case http.StatusForbidden:
			page, pageErr = pages.CreateForbiddenPage(cm, "open.menu#from=forbidden")

		case http.StatusNotFound:
			page, pageErr = pages.CreateNotFoundPage(cm, "open.menu#from=not_found")

		case http.StatusUnprocessableEntity:
			// Request body is invalid: incorrect group id, etc
			for _, field := range httpApiError.Err.(*api.ValidationError).Fields {
				switch field.Field {
				case "groupId":
					page, pageErr = pages.CreateInvalidGroupPage(cm)
				default:
					// Unknown field
					page, pageErr = pages.CreateErrorPage(cm)
					log.Errorf("Unknown validation error field: %s", field.Field)
					SendErrorToTelegram(err)
				}
			}
			if page == nil {
				// No fields in ValidationError
				page, pageErr = pages.CreateErrorPage(cm)
				log.Errorf("No fields in ValidationError: %s", err)
				SendErrorToTelegram(err)
			}

		default:
			// Unknown error
			page, pageErr = pages.CreateApiUnavailablePage(cm)

			if httpApiError.Code/100 != 5 {
				log.Errorf("Unknown API http status code %d: %s", httpApiError.Code, httpApiError.Body)
				SendErrorToTelegram(err)
			}
		}

		if pageErr != nil {
			log.Errorf("Error creating HTTPApiError page: %s", pageErr)
			SendErrorToTelegram(pageErr)
			break
		}

		if update.CallbackQuery != nil {
			_, err = settings.Bot.Send(buttons.EditMessageRequest(page, update.CallbackQuery))
		} else {
			_, err = settings.Bot.Send(page.CreateMessage(cm.ChatId))
		}

		if err != nil {
			log.Errorf("Error sending HTTPApiError page: %s", err)
			SendErrorToTelegram(err)
		}

	case errors.As(err, &tgError):
		// Telegram API error
		switch tgError.Code {
		case 403:
			// User blocked bot
			chat := update.FromChat()
			if chat == nil {
				break
			}

			// Get chat data
			cm := utils.GetChatDataManager(chat.ID)
			chatData, err := cm.GetChatData()
			if err != nil {
				log.Errorf("Error getting chat data: %s", err)
				SendErrorToTelegram(err)
				break
			}

			// Set chat data "accessible" to false
			chatData.Accessible = false
			err = cm.UpdateChatData(chatData)
			if err != nil {
				log.Errorf("Error updating chat data: %s", err)
				SendErrorToTelegram(err)
				break
			}
		case 420:
			// Flood control exceeded
			log.Warningf("Flood control exceeded, retry after %d: %s", tgError.RetryAfter, err)

			// Get chat where error occurred
			chat := update.FromChat()
			if chat == nil {
				break
			}

			// Send alert to chat
			if update.CallbackQuery == nil {
				// Can't edit message
				break
			}

			lang, err := utils.GetLang(utils.GetChatDataManager(chat.ID))
			if err != nil {
				log.Errorf("Error getting chat language: %s", err)
				break
			}

			text := format.Formatp(lang.Alert.FloodControl, tgError.ResponseParameters.RetryAfter)
			_, err = settings.Bot.Request(tgbotapi.NewCallbackWithAlert(update.CallbackQuery.ID, text))
			if err != nil {
				log.Errorf("Error sending flood control alert: %s", err)
				break
			}
		case 400:
			// Bad request
			if strings.HasPrefix(tgError.Message, "Bad Request: message is not modified") {
				// We are trying to edit message with no changes,
				// probably because of lag. Just send warning to log.
				log.Warningf("Message is not modified: %s", err)
				break
			}

			// Unknown Telegram API error
			log.Errorf("Unknown bad request error: %s", err)
			SendErrorToTelegram(err)
			SendErrorPageToChat(&update)

		default:
			// Unknown Telegram API error
			log.Errorf("Unknown Telegram API %d error: %s", tgError.Code, err)
			SendErrorToTelegram(err)
			SendErrorPageToChat(&update)
		}

	default:
		// Unknown error
		log.Errorf("Unknown error: %s", err)
		SendErrorToTelegram(err)
		SendErrorPageToChat(&update)
	}
}

func SendErrorToTelegram(err error) {
	chatId := os.Getenv("LOG_CHAT_ID")
	if chatId == "" {
		return
	}

	str := fmt.Sprintf("Error %T: %s", err, err)

	// Send error to Telegram
	_, err2 := settings.Bot.Send(tgbotapi.NewMessageToChannel(chatId, str))
	if err2 != nil {
		// Nothing we can do here, just log the error
		log.Errorf("Error sending error to Telegram: %s", err)
	}
}

func SendErrorPageToChat(update *tgbotapi.Update) {
	if update.FromChat() == nil {
		return
	}

	cm := utils.GetChatDataManager(update.FromChat().ID)
	page, err := pages.CreateErrorPage(cm)
	if err != nil {
		log.Errorf("Error creating error page: %s", err)
		SendErrorToTelegram(err)
		return
	}

	if update.CallbackQuery != nil {
		_, err = settings.Bot.Send(buttons.EditMessageRequest(page, update.CallbackQuery))
	} else {
		_, err = settings.Bot.Send(page.CreateMessage(cm.ChatId))
	}

	if err != nil {
		log.Errorf("Error sending error page: %s", err)
		SendErrorToTelegram(err)
		return
	}
}
