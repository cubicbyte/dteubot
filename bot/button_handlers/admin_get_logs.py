import os.path
from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..settings import LOGS_PATH

@register_button_handler(r'^admin.get_logs$')
async def handler(update: Update, context: CallbackContext):
    await context.bot.send_chat_action(update.effective_chat.id, 'upload_document', timeout=10)
    file = os.path.join(LOGS_PATH, 'debug.log')
    fp = open(file, 'rb')
    await context.bot.send_document(update.effective_chat.id, fp)
    fp.close()
