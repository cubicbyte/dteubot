import os
import time
import logging
import telebot.types
import bot.message_handlers
import bot.callback_query_handlers
from bot import modify_message
from bot.settings import bot, tg_logger

logger = logging.getLogger()
logger.info('Starting application')



@bot.middleware_handler(update_types=['message'])
def message_middleware(bot_instance, message: telebot.types.Message):
    # This applies to every new message
    # Adds methods to them to get the chat config, etc.
    logger.debug('Called modify message middleware')
    modify_message(message=message)

@bot.middleware_handler(update_types=['callback_query'])
def callback_query_middleware(bot_instance, call: telebot.types.CallbackQuery):
    # Same as above, but for button click
    logger.debug('Called main callback query middleware')
    modify_message(call=call)

# Calling a logger to write a message or button click to the logs for stats
bot.middleware_handler(update_types=['message'])(tg_logger.message_middleware)
bot.middleware_handler(update_types=['callback_query'])(tg_logger.callback_query_middleware)



# Run bot
if os.getenv('MODE') == 'prod':
    logger.info('Running in production mode')

    while True:
        logger.debug('Start polling')

        try:
            bot.polling(none_stop=True)

        except Exception as e:
            # Called when an internet connection or another error occurs.
            logger.error('Bot polling error: %s' % e)
            time.sleep(2)

elif os.getenv('MODE') == 'dev':
    logger.info('Running in dev mode')

    # In development mode, there is no error handler here
    while True:
        logger.debug('Start polling')
        bot.polling(none_stop=True)
