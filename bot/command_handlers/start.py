import logging
import telebot.types
from ..settings import bot, chat_configs
from ..pages import greeting, menu, select_structure

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /start command from chat %s' % message.chat.id)

    if message.config_created:
        bot.send_message(**greeting.create_message(message))
        bot.send_message(**menu.create_message(message))
        return

    if len(message.args_case) == 0:
        ref = None
    else:
        ref = message.args_case[0]
    chat_configs.set_chat_config_field(message.chat.id, 'ref', ref, True)

    bot.send_message(**greeting.create_message(message))
    bot.send_message(**select_structure.create_message(message))
