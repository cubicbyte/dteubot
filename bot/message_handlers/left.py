import logging
import telebot.types
from ..settings import bot
from ..messages import create_left_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['left'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /left command from chat %s' % message.chat.id)
    bot.send_message(**create_left_message(message))
