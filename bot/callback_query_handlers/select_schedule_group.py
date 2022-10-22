import telebot.types
import logging
from ..settings import bot, chat_configs
from ..messages import create_menu_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.data.startswith('select.schedule.group_id'))
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    group_id = int(call.data.split('=')[1])
    call.message.config['schedule']['group_id'] = group_id
    chat_configs.set_chat_config(call.message.chat.id, call.message.config)
    bot.edit_message_text(**create_menu_message(call.message), message_id=call.message.id)
