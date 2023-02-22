import telebot.types
import logging
from ..settings import bot
from ..pages import select_structure

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.select_group')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    bot.edit_message_text(**select_structure.create_message(call.message.lang_code), chat_id=call.message.chat.id, message_id=call.message.message_id)
