import telebot.types
import logging
from datetime import datetime, timedelta
from ..settings import bot
from ..messages import create_schedule_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.schedule.tomorrow')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    bot.edit_message_text(**create_schedule_message(call.message, date), message_id=call.message.message_id)
