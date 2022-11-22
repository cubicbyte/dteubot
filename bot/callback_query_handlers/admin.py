import telebot.types
import logging
from ..settings import bot

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query.startswith('admin') and call.user.config['admin'] is not True)
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling admin callback query')
    bot.answer_callback_query(
        text=call.message.lang['text.no_permissions'],
        callback_query_id=call.id,
        show_alert=True
    )
