import telebot.types
import logging
from ..settings import bot

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'admin.get_logs')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling admin callback query')
    bot.send_chat_action(call.message.chat.id, 'upload_document', timeout=10)
    f = open('logs/debug.log', 'rb')
    bot.send_document(call.message.chat.id, f)
    f.close()
