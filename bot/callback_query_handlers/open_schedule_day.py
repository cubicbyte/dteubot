import telebot.types
import logging
from ..settings import bot
from ..messages import create_schedule_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.schedule.day')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    date = call.args['date']
    bot.edit_message_text(**create_schedule_message(call.message, date), message_id=call.message.message_id)
