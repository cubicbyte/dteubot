import logging
import telebot.types
from ..settings import bot
from ..messages import create_calls_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['calls'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /calls command from chat %s' % message.chat.id)
    bot.send_message(**create_calls_message(message))
