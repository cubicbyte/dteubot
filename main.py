import logging

from telegram.ext import MessageHandler, CallbackQueryHandler
from bot.settings import bot, tg_logger, LOG_CHAT_ID
from bot.button_handlers import *
from bot.button_handlers import handlers as button_handlers, register_button_handler
from bot.command_handlers import *
from bot.command_handlers import handlers as command_handlers
from bot.pages import menu
from bot.data import UserData, ChatData
from bot import error_handler



error_handler.log_chat_id = LOG_CHAT_ID
logger = logging.getLogger()
logger.info('Starting application')

async def apply_data(upd, ctx):
    ctx._user_data = UserData(upd.effective_user.id)
    ctx._chat_data = ChatData(upd.effective_chat.id)

async def btn_handler(upd, ctx):
    logger.info('[chat/{0} user/{1} msg/{2}] callback query: {3}'.format(
        upd.callback_query.message.chat.id,
        upd.callback_query.from_user.id,
        upd.callback_query.message.id,
        upd.callback_query.data))
    await apply_data(upd, ctx)

async def msg_handler(upd, ctx):
    logger.info('[chat/{0} user/{1} msg/{2}] message: {3}'.format(
        upd.message.chat.id,
        upd.message.from_user.id,
        upd.message.id,
        upd.message.text))
    await apply_data(upd, ctx)

@register_button_handler()
async def unsupported_btn_handler(upd, ctx):
    await upd.callback_query.answer(ctx._chat_data.get_lang()['alert.callback_query_unsupported'], show_alert=True)
    await upd.callback_query.message.edit_text(**menu.create_message(ctx))

bot.add_handlers([CallbackQueryHandler(btn_handler), MessageHandler(None, msg_handler)])
bot.add_handlers(button_handlers + command_handlers, 10)
bot.add_handlers([CallbackQueryHandler(tg_logger.callback_query_handler), MessageHandler(None, tg_logger.message_handler)], 20)
bot.add_error_handler(error_handler.handler)


# Run bot
bot.run_polling()
