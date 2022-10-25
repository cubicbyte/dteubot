import logging
import telebot.types
from ..settings import bot
from ..messages import create_settings_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['settings'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /settings command from chat %s' % message.chat.id)
    bot.send_message(**create_settings_message(message))
