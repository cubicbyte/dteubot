import logging

# Update bot data to the latest version
from scripts.update_bot_data import main as update_bot_data
update_bot_data('.')


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

@register_button_handler()
async def unsupported_btn_handler(upd, ctx):
    await upd.callback_query.answer(ctx._chat_data.lang['alert.callback_query_unsupported'], show_alert=True)
    await upd.callback_query.message.edit_text(**menu.create_message(ctx))

bot.add_handlers([CallbackQueryHandler(apply_data), MessageHandler(None, apply_data)])
bot.add_handlers(button_handlers + command_handlers, 10)
bot.add_handlers([CallbackQueryHandler(tg_logger.callback_query_handler), MessageHandler(None, tg_logger.message_handler)], 20)
bot.add_error_handler(error_handler.handler)


# Run bot
bot.run_polling()
