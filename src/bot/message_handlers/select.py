import logging
import telebot.types
from ..settings import bot, chat_configs
from ..messages import create_menu_message, create_select_structure_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['select'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /select command from chat %s' % message.chat.id)
    
    if len(message.args) == 0:
        bot.send_message(**create_select_structure_message(message))
    else:
        group_id = message.args[0]

        if group_id.isnumeric():
            group_id = abs(int(group_id))
            message._config = chat_configs.set_chat_config_field(message.chat.id, 'groupId', group_id)

        bot.send_message(**create_menu_message(message))
