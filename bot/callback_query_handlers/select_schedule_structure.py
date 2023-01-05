import telebot.types
import logging
from ..settings import bot, chat_configs
from ..pages import select_faculty

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.schedule.structure')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    struct_id = int(call.args['structureId'])
    chat_configs.set_chat_config(call.message.chat.id, call.message.config)
    bot.edit_message_text(**select_faculty.create_message(call.message, struct_id), message_id=call.message.id)
