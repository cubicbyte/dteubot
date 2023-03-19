from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import info

@register_button_handler('^open.info$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(**info.create_message(context))
