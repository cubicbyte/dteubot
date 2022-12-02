import logging
import telebot.types
from datetime import date
from ..settings import bot
from ..pages import create_schedule_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['today'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /today command from chat %s' % message.chat.id)
    cur_date = date.today()
    bot.send_message(**create_schedule_message(message, cur_date.strftime('%Y-%m-%d')))
