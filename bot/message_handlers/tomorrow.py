import logging
import telebot.types
from datetime import datetime, timedelta
from ..settings import bot
from ..messages import create_schedule_message

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['tomorrow'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /tomorrow command from chat %s' % message.chat.id)
    date = datetime.today() + timedelta(days=1)
    bot.send_message(**create_schedule_message(message, date.strftime('%Y-%m-%d')))
