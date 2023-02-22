import logging
import telebot.types
from ..settings import bot
from ..pages import lang_select, menu

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['lang'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /lang command from chat %s' % message.chat.id)

    if len(message.args) == 0:
        bot.send_message(**lang_select.create_message(message.lang_code), chat_id=message.chat.id)
    else:
        message.lang_code = message.args[0]
        bot.send_message(**menu.create_message(message), chat_id=message.chat.id)
