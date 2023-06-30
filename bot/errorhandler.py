# pylint: disable=unused-argument

"""
Module for handling bot errors.
"""

import os
import logging
import traceback
from datetime import datetime

import telegram.error
from telegram import Update, Bot
from telegram.error import BadRequest, NetworkError, Forbidden, TimedOut
from telegram.ext import CallbackContext

from bot.data import ChatDataManager, ContextManager
from bot.pages import error as error_page
from bot.utils import smart_split

_logger = logging.getLogger(__name__)
log_chat_id: int | str = os.getenv('LOG_CHAT_ID')


async def handler(update: Update, context: CallbackContext):
    """Handle errors raised by the bot."""

    if hasattr(context, 'effective_chat'):
        chat_data = ChatDataManager(update.effective_chat.id)

    if isinstance(context.error, BadRequest):
        _logger.warning(context.error)
        if context.error.message.startswith('Message is not modified'):
            return
        if context.error.message.startswith('Chat not found') or \
                context.error.message.startswith('Peer_id_invalid'):
            chat_data.set('_accessible', False)
            return
        if context.error.message.startswith('Message can\'t be deleted for everyone'):
            if isinstance(context, CallbackContext):
                await update.callback_query.answer(text=chat_data.lang.get('alert.message_too_old'))
            return

    if isinstance(context.error, Forbidden):
        # Bot was blocked by the user
        _logger.warning(context.error)
        context.data.set('_accessible', False)
        return

    if isinstance(context.error, TimedOut) or \
            isinstance(context.error, NetworkError) \
            and context.error.message.startswith('httpx'):
        # telegram.ext._updater already logs this error
        return

    print(traceback.format_exc())
    _logger.exception(context.error)

    await send_error_to_telegram(context.bot, context.error)
    await send_error_response(update, context)


async def send_error_response(update: Update, context: CallbackContext):
    """Send an error page to the user as an error response."""

    ctx = ContextManager(update, context)
    page = error_page(ctx)

    if update.callback_query is not None:
        # If the error happened when clicking a button
        msg = await update.callback_query.edit_message_text(**page)
    else:
        # If the error happened when sending a command
        msg = await update.message.reply_text(**page)

    ctx.chat_data.save_message('error', msg)


async def send_error_to_telegram(bot: Bot, err: Exception):
    """Send an error message to the log chat."""

    if log_chat_id is not None:
        err_time = datetime.now().isoformat(sep=" ", timespec="seconds")
        for err_text in smart_split(f'[{err_time}] {traceback.format_exc()}'):
            try:
                await bot.send_message(chat_id=log_chat_id, text=err_text)
            except telegram.error.TelegramError:
                _logger.exception('Failed to send exception to log chat')
