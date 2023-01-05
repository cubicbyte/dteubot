import logging
import telebot.types
from ..settings import bot
from ..pages import create_lang_select_message, create_menu_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['lang'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /lang command from chat %s' % message.chat.id)

    if len(message.args) == 0:
        bot.send_message(**create_lang_select_message(message))
    else:
        message.lang_code = message.args[0]
        bot.send_message(**create_menu_message(message))
