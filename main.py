#!/usr/bin/env python3
# pylint: disable=wrong-import-position

"""
This is the main file of the bot.
"""

import os
import time
import asyncio
import logging

from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.ext import filters

from settings import *


# Create required directories
os.makedirs(os.getenv('LOGS_PATH'), exist_ok=True)
os.makedirs(os.getenv('USER_DATA_PATH'), exist_ok=True)
os.makedirs(os.getenv('CHAT_DATA_PATH'), exist_ok=True)


# Init logger
logger = logging.getLogger('bot')
logger.info('Starting application')


# Disable httpx GET request logging
logging.getLogger('httpx').setLevel(logging.WARNING)

_logger = logging.getLogger(__name__)
_logger.info('Running setup')

from bot import buttons as _
from bot import commands as _
from bot.buttons import handlers as button_handlers, register_button
from bot.commands import handlers as command_handlers
from bot.logger import TelegramLogger
from bot.data import ContextManager, ChatDataManager
from bot import errorhandler, pages
from settings import bot, NOTIFICATIONS_SUGGESTION_DELAY_S
from notifier import scheduler


async def set_chat_accessible(upd, ctx):
    # pylint: disable=unused-argument
    """Set chat accessibility"""

    chat_data = ChatDataManager(upd.effective_chat.id)

    if not chat_data.get('_accessible'):
        chat_data.set('_accessible', True)


async def log_button(upd, ctx):
    # pylint: disable=unused-argument
    """Log button clicks"""

    logger.info('[chat/%s user/%s msg/%s] callback query: %s',
        upd.callback_query.message.chat.id,
        upd.callback_query.from_user.id,
        upd.callback_query.message.id,
        upd.callback_query.data
    )


async def log_message(upd, ctx):
    # pylint: disable=unused-argument
    """Log messages"""

    logger.info('[chat/%s user/%s msg/%s] message: %s',
        upd.message.chat.id,
        upd.message.from_user.id,
        upd.message.id,
        upd.message.text
    )


async def button_statistic_logger(upd, ctx):
    """Save button clicks into statistics"""
    manager = ContextManager(upd, ctx)
    await tg_logger.callback_query_handler(manager)


async def message_statistic_logger(upd, ctx):
    """Save messages into statistics"""
    if not upd.effective_user:
        # Private message, most likely at channel
        # Ignore messages from channels
        return

    manager = ContextManager(upd, ctx)
    await tg_logger.message_handler(manager)


async def suggest_cl_notif(upd, ctx):
    """Suggest classes notifications to user"""

    # If chat is old enough and user haven't seen settings yet,
    # suggest him to enable notifications

    _ctx = ContextManager(upd, ctx)

    if not _ctx.chat_data.get('seen_settings'):
        cur_timestamp = int(time.time())
        created = _ctx.chat_data.get('_created') or 0

        if _ctx.chat_data.get('group_id') is None:
            return

        if cur_timestamp - created < NOTIFICATIONS_SUGGESTION_DELAY_S:
            return

        # After 1 second, send new message with notification suggestion
        await asyncio.sleep(1)

        msg = await upd.effective_message.reply_text(**pages.notification_feature_suggestion(_ctx))
        _ctx.chat_data.save_message('notification_feature_suggestion', msg)

        _ctx.chat_data.set('seen_settings', True)


@register_button()
async def unsupported_btn_handler(ctx):
    """Handle unsupported button"""

    await ctx.update.callback_query.answer(
        ctx.lang.get('alert.callback_query_unsupported'), show_alert=True)
    msg = await ctx.update.callback_query.message.edit_text(**pages.menu(ctx))
    ctx.chat_data.save_message('menu', msg)


tg_logger = TelegramLogger(os.path.join(os.getenv('LOGS_PATH'), 'telegram'))


# Register telegram button & command handlers

# Logging
bot.add_handlers([
    CallbackQueryHandler(log_button),
    MessageHandler(filters.COMMAND, log_message)], 0)
# Main handlers
bot.add_handlers(button_handlers + command_handlers, 10)
# Statistics
bot.add_handlers([
    CallbackQueryHandler(button_statistic_logger),
    MessageHandler(filters.TEXT, message_statistic_logger)], 20)
# Update chat accessibility
bot.add_handlers([
    CallbackQueryHandler(set_chat_accessible),
    MessageHandler(filters.COMMAND, set_chat_accessible)], 30)
# Notifications suggestion
bot.add_handlers([
    CallbackQueryHandler(suggest_cl_notif),
    MessageHandler(filters.COMMAND, suggest_cl_notif)], 40)

# Error handler
bot.add_error_handler(errorhandler.handler)


# Run classes notifications system
scheduler.start()
# Run bot
bot.run_polling()
