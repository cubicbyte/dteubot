import logging
import telebot.types
from ..settings import bot
from ..pages import statistic

logger = logging.getLogger(__name__)

@bot.message_handler(content_types=['text'], func=lambda msg: msg.text.startswith('/empty_'))
def handle_command(message: telebot.types.Message):
    logger.info('Handling /empty_* command from chat %s' % message.chat.id)
    bot.send_message(**statistic.create_message(message))
