import logging
import telebot.types
from datetime import datetime, timedelta
from ..settings import bot
from ..pages import schedule

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['tomorrow'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /tomorrow command from chat %s' % message.chat.id)
    date = datetime.today() + timedelta(days=1)
    bot.send_message(**schedule.create_message(message.lang_code, message.config['groupId'], date), chat_id=message.chat.id)
