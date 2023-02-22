import telebot.types
import logging
from ..pages import info
from ..settings import bot

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.info')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    bot.edit_message_text(**info.create_message(call.message.lang_code), chat_id=call.message.chat.id, message_id=call.message.message_id)
