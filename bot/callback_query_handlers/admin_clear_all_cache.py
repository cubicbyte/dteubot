import telebot.types
import logging
from ..settings import bot, api

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'admin.clear_all_cache')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling admin callback query')

    api._session.remove_expired_responses(expire_after=1)

    bot.answer_callback_query(
        text=call.message.lang['text.done'],
        callback_query_id=call.id,
        show_alert=True
    )
