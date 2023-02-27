import os
import logging
import telebot.types
from bot.command_handlers import *
from bot.button_handlers import *
from bot.modify_message import modify_message, modify_callback_query
from bot.settings import bot, tg_logger

logger = logging.getLogger()
logger.info('Starting application')


#from bot.pages import left
#print(left.create_message('uk', 741)['text'])
#exit(0)


@bot.middleware_handler(update_types=['message'])
def message_middleware(bot_instance, message: telebot.types.Message):
    # This applies to every new message
    # Adds methods to them to get the chat config, etc.
    logger.debug('Called modify message middleware')
    modify_message(message)

@bot.middleware_handler(update_types=['callback_query'])
def callback_query_middleware(bot_instance, call: telebot.types.CallbackQuery):
    # Same as above, but for button click
    logger.debug('Called main callback query middleware: %s' % call.data)
    modify_callback_query(call)



# Calling a logger to write a message or button click to the logs for stats
bot.middleware_handler(update_types=['message'])(tg_logger.message_middleware)
bot.middleware_handler(update_types=['callback_query'])(tg_logger.callback_query_middleware)



# Run bot
if os.getenv('MODE') == 'prod':
    logger.info('Running in production mode')
    bot.infinity_polling(allowed_updates=['message', 'callback_query'])

elif os.getenv('MODE') == 'dev':
    logger.info('Running in dev mode')

    # In development mode, there is no error handler here
    while True:
        logger.debug('Start polling')
        bot.polling(none_stop=True)
