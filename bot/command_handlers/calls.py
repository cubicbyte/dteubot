import logging
import telebot.types
from ..settings import bot
from ..pages import calls

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['calls'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /calls command from chat %s' % message.chat.id)
    bot.send_message(**calls.create_message(message.lang_code), chat_id=message.chat.id)
