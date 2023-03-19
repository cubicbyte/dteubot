from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import more

@register_button_handler('^open.more$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(**more.create_message(context))
