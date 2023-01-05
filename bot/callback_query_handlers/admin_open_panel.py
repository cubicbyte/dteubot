import telebot.types
import logging
from ..settings import bot
from ..pages import admin_panel

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'admin.open_panel')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling admin callback query')
    bot.edit_message_text(**admin_panel.create_message(call.message), message_id=call.message.message_id)
