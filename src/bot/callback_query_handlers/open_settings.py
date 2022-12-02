import telebot.types
import logging
from ..settings import bot
from ..pages import create_settings_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.settings')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    bot.edit_message_text(**create_settings_message(call.message), message_id=call.message.message_id)
