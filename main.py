import os
import asyncio
import logging
import settings
from telegram.ext import MessageHandler, CallbackQueryHandler
from bot.utils import load_langs


settings.langs = load_langs(os.getenv('LANGS_PATH'))
logger = logging.getLogger()
logger.info('Starting application')


from settings import bot, tg_logger
from bot.buttons import *
from bot.buttons import handlers as button_handlers, register_button
from bot.commands import *
from bot.commands import handlers as command_handlers
from bot.notification_scheduler import scheduler
from bot import error_handler, pages


async def set_chat_accessible(ctx):
    if not ctx.chat_data.get('_accessible'):
        ctx.chat_data.set('_accessible', True)


async def button_logger(ctx):
    logger.info('[chat/{0} user/{1} msg/{2}] callback query: {3}'.format(
        ctx.update.callback_query.message.chat.id,
        ctx.update.callback_query.from_user.id,
        ctx.update.callback_query.message.id,
        ctx.update.callback_query.data))


async def message_logger(ctx):
    logger.info('[chat/{0} user/{1} msg/{2}] message: {3}'.format(
        ctx.update.message.chat.id,
        ctx.update.message.from_user.id,
        ctx.update.message.id,
        ctx.update.message.text))


@register_button()
async def unsupported_btn_handler(ctx):
    await ctx.update.callback_query.answer(ctx.lang.get('alert.callback_query_unsupported'), show_alert=True)
    msg = await ctx.update.callback_query.message.edit_text(**pages.menu(ctx))
    ctx.chat_data.save_message('menu', msg)


async def suggest_notif_feature(upd, ctx):
    if not ctx.chat_data.get('cl_notif_suggested') and ctx.chat_data.get('_created') == 0:
        await asyncio.sleep(1)
        msg = await upd.effective_message.reply_text(**pages.notification_feature_suggestion(ctx))
        ctx.chat_data.save_message('notification_feature_suggestion', msg)
        ctx.chat_data.set('cl_notif_suggested', True)


bot.add_handlers([CallbackQueryHandler(button_logger), MessageHandler(None, message_logger)], 0)
bot.add_handlers([CallbackQueryHandler(set_chat_accessible), MessageHandler(None, set_chat_accessible)], 5)
bot.add_handlers(button_handlers + command_handlers, 10)
bot.add_handlers([CallbackQueryHandler(suggest_notif_feature), MessageHandler(None, suggest_notif_feature)], 15)
bot.add_handlers([CallbackQueryHandler(tg_logger.callback_query_handler), MessageHandler(None, tg_logger.message_handler)], 20)
bot.add_error_handler(error_handler.handler)


# Run notifications scheduler
scheduler.start()
# Run bot
bot.run_polling()
