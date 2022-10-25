import telebot.types
import logging
from ..settings import bot
from ..messages import create_select_structure_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.data.startswith('open.select_group'))
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    bot.edit_message_text(**create_select_structure_message(call.message), message_id=call.message.message_id)
