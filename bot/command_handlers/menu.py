import logging
import telebot.types
from ..settings import bot
from ..pages import menu

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['menu'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /menu command from chat %s' % message.chat.id)
    bot.send_message(**menu.create_message(message), chat_id=message.chat.id)
