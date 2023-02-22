import telebot.types
import logging
from ..settings import bot, chat_configs
from ..pages import select_faculty

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.schedule.structure')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    struct_id = int(call.args['structureId'])
    bot.edit_message_text(**select_faculty.create_message(call.message.lang_code, struct_id), chat_id=call.message.chat.id, message_id=call.message.id)
