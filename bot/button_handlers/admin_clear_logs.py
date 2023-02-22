import telebot.types
import logging
import os.path
from ..settings import bot, LOGS_PATH
from ..utils.fs import create_file

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'admin.clear_logs')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling admin callback query')

    create_file(os.path.join(LOGS_PATH, 'debug.log'))

    bot.answer_callback_query(
        text=call.message.lang['alert.done'],
        callback_query_id=call.id,
        show_alert=True
    )
