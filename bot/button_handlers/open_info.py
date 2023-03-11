from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import info

@register_button_handler(r'^open.info$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(**info.create_message(context))
