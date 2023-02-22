import logging
import telebot.types
from datetime import date
from ..settings import bot
from ..pages import schedule

logger = logging.getLogger(__name__)

@bot.message_handler(commands=['today'])
def handle_command(message: telebot.types.Message):
    logger.info('Handling /today command from chat %s' % message.chat.id)
    bot.send_message(**schedule.create_message(message.lang_code, message.config['groupId'], date.today()), chat_id=message.chat.id)
