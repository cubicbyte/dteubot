from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler

@register_button_handler('^close_page$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.delete_message()
    context._chat_data.remove_message(update.callback_query.message.message_id)
