import telebot.types
import logging
import os.path
from ..settings import bot, LOGS_PATH
from ..utils.fs import open_file

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'admin.get_logs')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling admin callback query')
    bot.send_chat_action(call.message.chat.id, 'upload_document', timeout=10)
    path = os.path.join(LOGS_PATH, 'debug.log')
    f = open_file(path, 'rb')
    bot.send_document(call.message.chat.id, f)
    f.close()
