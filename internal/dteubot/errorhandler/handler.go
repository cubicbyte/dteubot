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
	"context"
	"errors"
	"fmt"
	"github.com/PaulSonOfLars/gotgbot/v2"
	"github.com/PaulSonOfLars/gotgbot/v2/ext"
	"github.com/cubicbyte/dteubot/internal/dteubot/pages"
	"github.com/cubicbyte/dteubot/internal/dteubot/utils"
	"github.com/cubicbyte/dteubot/internal/i18n"
	"github.com/cubicbyte/dteubot/pkg/api"
	"github.com/go-telegram/bot"
	"github.com/go-telegram/bot/models"
	"github.com/op/go-logging"
	"github.com/sirkon/go-format/v2"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

// ErrorSendDelay is the delay between sending errors to Telegram
const ErrorSendDelay = time.Second * 5

var log = logging.MustGetLogger("ErrorHandler")
var lastErrorTime time.Time

func HandleError(b *gotgbot.Bot, ctx *ext.Context, err error) ext.DispatcherAction {
	var urlError *url.Error
	var httpApiError *api.HTTPApiError
	var tgError *gotgbot.TelegramError

	switch {
	case errors.As(err, &urlError):
		// Can't make request to the university API

		tgChat := utils.GetUpdChat(update)
		if tgChat == nil {
			// Api error with no chat
			log.Errorf("Api request error with no chat: %s", err)
			SendErrorToTelegram(ctx, err, bot2)
			break
		}

		page, err := pages.CreateApiUnavailablePage(lang)
		if err != nil {
			log.Errorf("Error creating api unavailable page: %s", err)
			SendErrorToTelegram(ctx, err, bot2)
			break
		}

		if update.CallbackQuery != nil {
			params := page.CreateEditMessage(tgChat.ID, update.CallbackQuery.Message.ID)
			_, err = bot2.EditMessageText(ctx, &params)
		} else {
			params := page.CreateMessage(tgChat.ID)
			_, err = bot2.SendMessage(ctx, &params)
		}

		if err != nil {
			log.Errorf("Error sending api unavailable page: %s", err)
			SendErrorToTelegram(ctx, err, bot2)
		}
	case errors.As(err, &httpApiError):
		// Non-200 api status code

		tgChat := utils.GetUpdChat(update)
		if tgChat == nil {
			// Api error with no chat
			log.Errorf("Api error with no chat: %s", err)
			SendErrorToTelegram(ctx, err, bot2)
			break
		}

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
					SendErrorToTelegram(ctx, err, bot2)
				}
			}
			if page == nil {
				// No fields in ValidationError
				page, pageErr = pages.CreateErrorPage(lang)
				log.Errorf("No fields in ValidationError: %s", err)
				SendErrorToTelegram(ctx, err, bot2)
			}

		default:
			// Unknown error
			page, pageErr = pages.CreateApiUnavailablePage(lang)

			if httpApiError.Code/100 != 5 {
				log.Errorf("Unknown API http status code %d: %s", httpApiError.Code, httpApiError.Body)
				SendErrorToTelegram(ctx, err, bot2)
			}
		}

		if pageErr != nil {
			log.Errorf("Error creating HTTPApiError page: %s", pageErr)
			SendErrorToTelegram(ctx, pageErr, bot2)
			break
		}

		if update.CallbackQuery != nil {
			params := page.CreateEditMessage(tgChat.ID, update.CallbackQuery.Message.ID)
			_, err = bot2.EditMessageText(ctx, &params)
		} else {
			params := page.CreateMessage(tgChat.ID)
			_, err = bot2.SendMessage(ctx, &params)
		}

		if err != nil {
			log.Errorf("Error sending HTTPApiError page: %s", err)
			SendErrorToTelegram(ctx, err, bot2)
		}

	case errors.As(err, &tgError):
		// Telegram API error
		switch tgError.Code {
		case 403:
			// User blocked bot
			// Set chat data "accessible" to false
			chat.Accessible = false
			err = chatRepo.Update(chat)
			if err != nil {
				log.Errorf("Error updating chat data: %s", err)
				SendErrorToTelegram(ctx, err, bot2)
				break
			}
		case 420:
			// Flood control exceeded
			log.Warningf("Flood control exceeded, retry after %d: %s", tgError.RetryAfter, err)

			// Send alert to chat
			if update.CallbackQuery == nil {
				// Can't edit message
				break
			}

			text := format.Formatp(lang.Alert.FloodControl, tgError.ResponseParameters.RetryAfter)
			_, err = bot2.AnswerCallbackQuery(ctx, &bot.AnswerCallbackQueryParams{
				CallbackQueryID: update.CallbackQuery.ID,
				Text:            text,
			})
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

			if strings.HasPrefix(tgError.Message, "Bad Request: message to edit not found") {
				// Message to edit not found
				log.Warningf("Message to edit not found: %s", err)
				break
			}

			if strings.HasPrefix(tgError.Message, "Bad Request: message can't be deleted for everyone") {
				// We are trying to delete message that is older than 48 hours
				log.Warningf("Message can't be deleted for everyone: %s", err)
				break
			}

			// Unknown Telegram API error
			log.Errorf("Unknown bad request error: %s", err)
			SendErrorToTelegram(ctx, err, bot2)
			SendErrorPageToChat(ctx, update, bot2, lang)

		default:
			// Unknown Telegram API error
			log.Errorf("Unknown Telegram API %d error: %s", tgError.Code, err)
			SendErrorToTelegram(ctx, err, bot2)
			SendErrorPageToChat(ctx, update, bot2, lang)
		}

	default:
		// Unknown error
		log.Errorf("Unknown error: %s", err)
		SendErrorToTelegram(ctx, err, bot2)
		SendErrorPageToChat(ctx, update, bot2, lang)
	}
}

func SendErrorToTelegram(ctx context.Context, err error, bot2 *bot.Bot) {
	// Don't send errors too often
	if time.Since(lastErrorTime) < ErrorSendDelay {
		return
	}

	chatId := os.Getenv("LOG_CHAT_ID")
	if chatId == "" {
		return
	}

	errStr := fmt.Sprintf("Error %T: %s", err, err)

	// Send error to Telegram
	_, err2 := bot2.SendMessage(ctx, &bot.SendMessageParams{
		ChatID: chatId,
		Text:   errStr,
	})
	if err2 != nil {
		// Nothing we can do here, just log the error
		log.Errorf("Error sending error to Telegram: %s", err)
	}

	lastErrorTime = time.Now()
}

func SendErrorPageToChat(ctx context.Context, update *models.Update, bot2 *bot.Bot, lang *i18n.Language) {
	if utils.GetUpdChat(update) == nil {
		return
	}

	page, err := pages.CreateErrorPage(lang)
	if err != nil {
		log.Errorf("Error creating error page: %s", err)
		SendErrorToTelegram(ctx, err, bot2)
		return
	}

	if update.CallbackQuery != nil {
		params := page.CreateEditMessage(update.CallbackQuery.Message.Chat.ID, update.CallbackQuery.Message.ID)
		_, err = bot2.EditMessageText(ctx, &params)
	} else {
		params := page.CreateMessage(utils.GetUpdChat(update).ID)
		_, err = bot2.SendMessage(ctx, &params)
	}

	if err != nil {
		log.Errorf("Error sending error page: %s", err)
		SendErrorToTelegram(ctx, err, bot2)
		return
	}
}
