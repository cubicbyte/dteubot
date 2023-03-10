import logging
from telegram.ext import MessageHandler, CallbackQueryHandler
from bot.button_handlers import *
from bot.button_handlers import handlers as button_handlers
from bot.command_handlers import *
from bot.command_handlers import handlers as command_handlers
from bot.settings import bot, tg_logger
from bot.data import UserData, ChatData

#
# TODO validate user permissions on admin button click
# TODO update requirements
# TODO add a separate menu to respond to unsupported callback queries
#

logger = logging.getLogger()
logger.info('Starting application')

async def apply_data(upd, ctx):
    ctx._user_data = UserData(upd.effective_user.id)
    ctx._chat_data = ChatData(upd.effective_chat.id)

bot.add_handlers([CallbackQueryHandler(apply_data), MessageHandler(None, apply_data)])
bot.add_handlers(button_handlers, 10)
bot.add_handlers(command_handlers, 20)
bot.add_handlers([CallbackQueryHandler(tg_logger.callback_query_handler), MessageHandler(None, tg_logger.message_handler)], 30)



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
