import telebot.types
import logging
from ..settings import bot, chat_configs
from ..pages import create_menu_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.schedule.group')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    group_id = int(call.args['groupId'])
    call.chat.config['groupId'] = chat_configs.set_chat_config_field(call.message.chat.id, 'groupId', group_id)
    bot.edit_message_text(**create_menu_message(call.message), message_id=call.message.id)
