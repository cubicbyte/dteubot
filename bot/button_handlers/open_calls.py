import telebot.types
import logging
from ..settings import bot
from ..pages import calls

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.calls')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    bot.edit_message_text(**calls.create_message(call.message), message_id=call.message.message_id)
