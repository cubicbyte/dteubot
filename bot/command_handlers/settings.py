import logging
import telebot.types
from ..settings import bot
from ..pages import settings

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['settings'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /settings command from chat %s' % message.chat.id)
    bot.send_message(**settings.create_message(message.lang_code, message.config['groupId']), chat_id=message.chat.id)
