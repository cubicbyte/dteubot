import os
import logging
from bot.command_handlers import *
from bot.command_handlers import handlers
#from bot.button_handlers import *
#from bot.modify_message import modify_message, modify_callback_query
from bot.settings import bot, langs, api, chat_configs#, tg_logger

logger = logging.getLogger()
logger.info('Starting application')

bot.bot_data = {
    'langs': langs,
    'api': api,
    'config': chat_configs
}

bot.add_handlers(handlers)

# Calling a logger to write a message or button click to the logs for stats
# TODO
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
