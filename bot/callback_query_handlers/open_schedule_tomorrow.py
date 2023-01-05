import telebot.types
import logging
from datetime import datetime, timedelta
from ..settings import bot
from ..pages import schedule

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.schedule.tomorrow')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    bot.edit_message_text(**schedule.create_message(call.message, date), message_id=call.message.message_id)
