import logging
import telebot.types
from ..settings import bot, chat_configs
from ..pages import create_menu_message, create_select_structure_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /start command from chat %s' % message.chat.id)

    if message.config_created:
        bot.send_message(**create_menu_message(message))
        return

    if len(message.args_case) == 0:
        ref = None
    else:
        ref = message.args_case[0]

    chat_configs.set_chat_config_field(message.chat.id, 'ref', ref, True)
    bot.send_message(**create_select_structure_message(message))
