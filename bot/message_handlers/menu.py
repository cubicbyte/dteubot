import logging
import telebot.types
from ..settings import bot
from ..pages import create_menu_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['menu'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /menu command from chat %s' % message.chat.id)
    bot.send_message(**create_menu_message(message))
