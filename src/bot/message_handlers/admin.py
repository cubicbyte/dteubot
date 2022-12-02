import logging
import telebot.types
from ..settings import bot
from ..messages import create_admin_panel_message, create_access_denied_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['admin'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /admin command from chat %s' % message.chat.id)
    
    if message.config['admin'] is not True:
        return bot.send_message(**create_access_denied_message(message))

    bot.send_message(**create_admin_panel_message(message))
