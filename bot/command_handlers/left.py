import logging
import telebot.types
from ..settings import bot
from ..pages import left

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['left'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /left command from chat %s' % message.chat.id)
    bot.send_message(**left.create_message(message.lang_code, message.config['groupId']), chat_id=message.chat.id)
