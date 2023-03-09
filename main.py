import os
import logging
from telegram.ext import MessageHandler, CallbackQueryHandler, ContextTypes
from bot.command_handlers import *
from bot.command_handlers import handlers as command_handlers
from bot.button_handlers import *
from bot.button_handlers import handlers as button_handlers
from bot.settings import bot, tg_logger
from bot.data import BotData, UserData, ChatData

#
# TODO validate user permissions on admin button click
#

#import telegram
#b = telegram.Bot('')

logger = logging.getLogger()
logger.info('Starting application')

async def apply_data(update, context: ContextTypes.DEFAULT_TYPE):
    context._user_data = UserData(update.effective_user.id)
    context._chat_data = ChatData(update.effective_chat.id)

bot.bot_data = BotData
bot.add_handlers([MessageHandler(None, apply_data), CallbackQueryHandler(apply_data)])
bot.add_handlers(command_handlers, 10)
bot.add_handlers(button_handlers, 10)

# Calling a logger to write a message or button click to the logs for stats
# TODO apply this with lowest priority
#bot.middleware_handler(update_types=['message'])(tg_logger.message_middleware)
#bot.middleware_handler(update_types=['callback_query'])(tg_logger.callback_query_middleware)



# Run bot
# TODO
#if os.getenv('MODE') == 'prod':
#    logger.info('Running in production mode')
#    bot.infinity_polling(allowed_updates=['message', 'callback_query'])
#
#elif os.getenv('MODE') == 'dev':
#    logger.info('Running in dev mode')
#
#    # In development mode, there is no error handler here
#    while True:
#        logger.debug('Start polling')
#        bot.polling(none_stop=True)
bot.run_polling()
