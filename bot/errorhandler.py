# pylint: disable=unused-argument

"""
Module for handling bot errors.
"""

import os
import logging
import traceback
from datetime import datetime, timedelta

import telegram.error
from telegram import Update, Bot
from telegram.error import BadRequest, NetworkError, Forbidden, TimedOut, Conflict
from telegram.ext import CallbackContext

from bot.data import ChatDataManager, ContextManager
from bot.pages import error as error_page
from bot.utils import smart_split

_logger = logging.getLogger(__name__)
_last_conflict_time = datetime(1970, 1, 1)
log_chat_id: int | str = os.getenv('LOG_CHAT_ID')


async def handler(update: Update, context: CallbackContext):
    """Handle errors raised by the bot."""

    try:
        raise context.error

    except BadRequest:
        _logger.warning(context.error)

        if hasattr(update, 'effective_chat'):
            chat_data = ChatDataManager(update.effective_chat.id)

        if context.error.message.startswith('Message is not modified'):
            # User was clicking buttons too fast
            pass

        elif context.error.message.startswith('Chat not found') or \
                context.error.message.startswith('Peer_id_invalid'):
            # Chat was deleted most likely
            chat_data.set('_accessible', False)

        elif context.error.message.startswith('Message can\'t be deleted for everyone'):
            # Mostly occurs when the message is older than 48 hours
            if isinstance(context, CallbackContext):
                await update.callback_query.answer(text=chat_data.lang.get('alert.message_too_old'))

    except Forbidden:
        # Bot was blocked by the user
        _logger.warning(context.error)
        context.data.set('_accessible', False)
        return

    except TimedOut:
        # Problem with my server network
        pass

    except NetworkError:
        if context.error.message.startswith('httpx'):
            # telegram.ext._updater already logs this error
            pass
        else:
            _logger.exception(context.error)
            await send_error_to_telegram(context.bot, context.error)

    except Conflict:
        # Multiple instances of the bot are running
        global _last_conflict_time
        if datetime.now() - _last_conflict_time < timedelta(days=1):  # Prevent random conflict error
            _logger.exception(context.error)
            await send_error_to_telegram(context.bot, context.error)
        else:
            _logger.warning(context.error)

        _last_conflict_time = datetime.now()

    except:
        # Unknown error
        print(traceback.format_exc())
        _logger.exception(context.error)

        await send_error_to_telegram(context.bot)
        await send_error_response_to_user(update, context)


async def send_error_response_to_user(update: Update, context: CallbackContext):
    """Send an error page to the user as an error response."""

    if not hasattr(update, 'effective_chat'):
        return

    ctx = ContextManager(update, context)
    page = error_page(ctx)

    if update.callback_query is not None:
        # If the error happened when clicking a button
        msg = await update.callback_query.edit_message_text(**page)
    else:
        # If the error happened when sending a command
        msg = await update.message.reply_text(**page)

    ctx.chat_data.save_message('error', msg)


async def send_error_to_telegram(bot: Bot, err: Exception | str | None = None):
    """Send an error message to the log chat."""

    if log_chat_id is not None:
        error = traceback.format_exc() if err is None else str(err)
        err_time = datetime.now().isoformat(sep=" ", timespec="seconds")

        for err_text in smart_split(f'[{err_time}] {error}'):
            try:
                await bot.send_message(chat_id=log_chat_id, text=err_text)
            except telegram.error.TelegramError:
                _logger.exception('Failed to send exception to log chat')
