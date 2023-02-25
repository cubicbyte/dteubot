import telebot.types
import logging
from datetime import date
from ..settings import bot
from ..pages import schedule

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'open.schedule.today')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    bot.edit_message_text(**schedule.create_message(call.message.lang_code, call.message.config['groupId'], date.today()), chat_id=call.message.chat.id, message_id=call.message.message_id)
