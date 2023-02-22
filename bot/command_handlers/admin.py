import logging
import telebot.types
from ..settings import bot
from ..pages import admin_panel, access_denied

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['admin'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /admin command from chat %s' % message.chat.id)

    if message.config['admin'] is not True:
        return bot.send_message(**access_denied.create_message(message.lang_code), chat_id=message.chat.id)

    bot.send_message(**admin_panel.create_message(message.lang_code), chat_id=message.chat.id)
