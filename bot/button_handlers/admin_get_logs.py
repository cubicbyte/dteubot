import os.path
from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler, validate_admin
from settings import LOGS_PATH


@register_button_handler('^admin.get_logs$')
@validate_admin
async def handler(update: Update, context: CallbackContext):
    await context.bot.send_chat_action(update.callback_query.message.chat.id, 'upload_document')

    filepath = os.path.join(LOGS_PATH, 'debug.log')
    with open(filepath, 'rb') as file:
        await context.bot.send_document(update.callback_query.message.chat.id, file)
