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

package errorhandler

import (
	"errors"
	"fmt"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/data"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	"github.com/op/go-logging"
	"github.com/sirkon/go-format/v2"
	"net/http"
	"net/url"
	"os"
	"strconv"
	"strings"
	"time"
)

// ErrorSendDelay is the delay between sending errors to Telegram
const ErrorSendDelay = time.Second * 5

var log = logging.MustGetLogger("ErrorHandler")
var lastErrorTime time.Time

var (
	langs    map[string]i18n.Language
	chatRepo data.ChatRepository
)

// Setup sets up error handler
func Setup(langs2 map[string]i18n.Language, chatRepo2 data.ChatRepository) {
	langs = langs2
	chatRepo = chatRepo2
}

func HandleError(b *gotgbot.Bot, ctx *ext.Context, err error) ext.DispatcherAction {
	var urlError *url.Error
	var httpApiError *api.HTTPApiError
	var tgError *gotgbot.TelegramError

	// Get update chat data
	if ctx.EffectiveChat == nil {
		log.Errorf("Error %T with no chat: %s", err, err)
		SendErrorToTelegram(err, b)
		return ext.DispatcherActionEndGroups
	}

	chatData, err := chatRepo.GetById(ctx.EffectiveChat.Id)
	if err != nil {
		log.Errorf("Error getting chat data: %s", err)
		SendErrorToTelegram(err, b)
		return ext.DispatcherActionNoop
	}

	// Get chat language
	lang, err := utils.GetLang(chatData.LanguageCode, langs)
	if err != nil {
		log.Errorf("Error getting language: %s", err)
		SendErrorToTelegram(err, b)
		return ext.DispatcherActionNoop
	}

	switch {
	case errors.As(err, &urlError):
		// Can't make request to the university API

		// Send "API unavailable" page
		page, err := pages.CreateApiUnavailablePage(lang)
		if err != nil {
			log.Errorf("Error creating api unavailable page: %s", err)
			SendErrorToTelegram(err, b)
			break
		}

		SendPageToChat(ctx, b, page)
	case errors.As(err, &httpApiError):
		// Non-200 api status code

		log.Warningf("Api %d error: %s", httpApiError.Code, httpApiError.Body)

		var page *pages.Page
		var pageErr error

		switch httpApiError.Code {
		case http.StatusUnauthorized:
			page, pageErr = pages.CreateForbiddenPage(lang, "open.menu#from=unauthorized")

		case http.StatusInternalServerError:
			page, pageErr = pages.CreateApiUnavailablePage(lang)

		case http.StatusForbidden:
			page, pageErr = pages.CreateForbiddenPage(lang, "open.menu#from=forbidden")

		case http.StatusNotFound:
			page, pageErr = pages.CreateNotFoundPage(lang, "open.menu#from=not_found")

		case http.StatusUnprocessableEntity:
			// Request body is invalid: incorrect group id, etc
			for _, field := range httpApiError.Err.(*api.ValidationError).Fields {
				switch field.Field {
				case "groupId":
					page, pageErr = pages.CreateInvalidGroupPage(lang)
				default:
					// Unknown field
					page, pageErr = pages.CreateErrorPage(lang)
					log.Errorf("Unknown validation error field: %s", field.Field)
					SendErrorToTelegram(err, b)
				}
			}
			if page == nil {
				// No fields in ValidationError
				page, pageErr = pages.CreateErrorPage(lang)
				log.Errorf("No fields in ValidationError: %s", err)
				SendErrorToTelegram(err, b)
			}

		default:
			// Unknown error
			page, pageErr = pages.CreateApiUnavailablePage(lang)

			if httpApiError.Code/100 != 5 {
				log.Errorf("Unknown API http status code %d: %s", httpApiError.Code, httpApiError.Body)
				SendErrorToTelegram(err, b)
			}
		}

		if pageErr != nil {
			log.Errorf("Error creating HTTPApiError page: %s", pageErr)
			SendErrorToTelegram(pageErr, b)
			break
		}

		SendPageToChat(ctx, b, page)

	case errors.As(err, &tgError):
		// Telegram API error
		switch tgError.Code {
		case 403:
			// User blocked bot
			// Set chat data "accessible" to false
			chatData.Accessible = false
			err = chatRepo.Update(chatData)
			if err != nil {
				log.Errorf("Error updating chat data: %s", err)
				SendErrorToTelegram(err, b)
				break
			}
		case 420:
			// Flood control exceeded
			log.Warningf("Flood control exceeded, retry after %d: %s", tgError.ResponseParams.RetryAfter, err)

			// Send alert to chat
			if ctx.CallbackQuery == nil {
				// Can't edit message
				break
			}

			text := format.Formatp(lang.Alert.FloodControl, tgError.ResponseParams.RetryAfter)
			_, err = b.AnswerCallbackQuery(ctx.CallbackQuery.Id, &gotgbot.AnswerCallbackQueryOpts{
				Text: text,
			})

			if err != nil {
				log.Errorf("Error sending flood control alert: %s", err)
				break
			}
		case 400:
			// Bad request
			// TODO: test this
			if strings.HasPrefix(tgError.Description, "Bad Request: message is not modified") {
				// We are trying to edit message with no changes,
				// probably because of lag. Just send warning to log.
				log.Warningf("Message is not modified: %s", err)
				break
			}

			if strings.HasPrefix(tgError.Description, "Bad Request: message to edit not found") {
				// Message to edit not found
				log.Warningf("Message to edit not found: %s", err)
				break
			}

			if strings.HasPrefix(tgError.Description, "Bad Request: message can't be deleted for everyone") {
				// We are trying to delete message that is older than 48 hours
				log.Warningf("Message can't be deleted for everyone: %s", err)
				break
			}

			// Unknown Telegram API error
			log.Errorf("Unknown bad request error: %s", err)
			SendErrorToTelegram(err, b)
			SendErrorPageToChat(ctx, b, lang)

		default:
			// Unknown Telegram API error
			log.Errorf("Unknown Telegram API %d error: %s", tgError.Code, err)
			SendErrorToTelegram(err, b)
			SendErrorPageToChat(ctx, b, lang)
		}

	default:
		// Unknown error
		log.Errorf("Unknown error: %s", err)
		SendErrorToTelegram(err, b)
		SendErrorPageToChat(ctx, b, lang)
	}

	return ext.DispatcherActionEndGroups
}

func SendErrorToTelegram(err error, bot *gotgbot.Bot) {
	// Don't send errors too often
	if time.Since(lastErrorTime) < ErrorSendDelay {
		return
	}

	// Get chat id to send error to
	chatIdStr := os.Getenv("LOG_CHAT_ID")
	if chatIdStr == "" {
		return
	}

	chatId, err := strconv.ParseInt(chatIdStr, 10, 64)
	if err != nil {
		log.Errorf("Error parsing LOG_CHAT_ID: %s", err)
		return
	}

	// Send error to Telegram
	errStr := fmt.Sprintf("Error %T: %s", err, err)

	_, err2 := bot.SendMessage(chatId, errStr, nil)
	if err2 != nil {
		log.Errorf("Error sending error to Telegram: %s", err)
	}

	lastErrorTime = time.Now()
}

func SendErrorPageToChat(ctx2 *ext.Context, bot *gotgbot.Bot, lang *i18n.Language) {
	if ctx2.EffectiveChat == nil {
		log.Errorf("Error sending error page: no chat")
		return
	}

	page, err := pages.CreateErrorPage(lang)
	if err != nil {
		log.Errorf("Error creating error page: %s", err)
		SendErrorToTelegram(err, bot)
		return
	}

	SendPageToChat(ctx2, bot, page)
}

// SendPageToChat sends the given page to the chat of the given update.
// It either edits the message or sends a new one.
func SendPageToChat(ctx2 *ext.Context, bot *gotgbot.Bot, page *pages.Page) {
	var err error

	if ctx2.CallbackQuery != nil {
		opts := page.CreateEditMessageOpts(ctx2.EffectiveChat.Id, ctx2.EffectiveMessage.MessageId)
		_, _, err = bot.EditMessageText(page.Text, &opts)
	} else {
		opts := page.CreateSendMessageOpts()
		_, err = bot.SendMessage(ctx2.EffectiveChat.Id, page.Text, &opts)
	}

	if err != nil {
		log.Errorf("Error sending page: %s", err)
		SendErrorToTelegram(err, bot)
	}
}
