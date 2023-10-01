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
from telegram.error import BadRequest, NetworkError, Forbidden, TimedOut, Conflict, RetryAfter
from telegram.ext import CallbackContext

from bot.data import ChatDataManager, ContextManager
from bot.pages import error as error_page, menu as menu_page
from bot.utils import smart_split

_logger = logging.getLogger(__name__)
_last_conflict_time = datetime(1970, 1, 1)
log_chat_id: int | str = os.getenv('LOG_CHAT_ID')


async def handler(update: Update, context: CallbackContext):
    """Handle errors raised by the bot."""

    try:
        raise context.error

    except BadRequest:
        if hasattr(update, 'effective_chat'):
            chat_data = ChatDataManager(update.effective_chat.id)

        if context.error.message.startswith('Message is not modified'):
            # User was clicking buttons too fast
            _logger.warning(context.error)
            pass

        elif context.error.message.startswith('Chat not found') or \
                context.error.message.startswith('Peer_id_invalid'):
            # Chat was deleted most likely
            _logger.warning(context.error)
            chat_data.set('_accessible', False)

        elif context.error.message.startswith('Message can\'t be deleted for everyone'):
            # Mostly occurs when the message is older than 48 hours
            if isinstance(context, CallbackContext):
                _logger.warning(context.error)
                await update.callback_query.answer(text=chat_data.lang.get('alert.message_too_old'))
                page = menu_page(ContextManager(update, context))
                msg = await update.callback_query.edit_message_text(**page)
                chat_data.remove_message(msg.id)
                chat_data.save_message('menu', msg)

        else:
            # Unknown error
            _logger.exception(context.error)
            await send_error_to_telegram(context.bot, context.error)
            await send_error_response_to_user(update, context)

    except RetryAfter:
        # Flood control
        _logger.warning(context.error)

        if isinstance(context, CallbackContext):
            chat_data = ChatDataManager(update.effective_chat.id)
            await update.callback_query.answer(text=chat_data.lang.get('alert.flood_control').format(context.error.retry_after))

    except Forbidden:
        # Bot most likely was blocked by the user
        if context.error.message.startswith('Forbidden: bot was blocked by the user'):
            chat_data = ChatDataManager(update.effective_chat.id)
            chat_data.set('_accessible', False)
            _logger.warning(context.error)
        else:
            # Unknown error
            _logger.exception(context.error)
            await send_error_to_telegram(context.bot)

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
        ctx.chat_data.remove_message(msg.id)
    else:
        # If the error happened when sending a command
        if update.effective_message is None:
            return
        msg = await update.effective_message.reply_text(**page)

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
