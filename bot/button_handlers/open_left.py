from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import left

@register_button_handler('^open.left$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(**left.create_message(context))
