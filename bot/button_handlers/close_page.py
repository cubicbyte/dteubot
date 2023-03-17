from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler

@register_button_handler(r'^close_page$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.delete_message()
