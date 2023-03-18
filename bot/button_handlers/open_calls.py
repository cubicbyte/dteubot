from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import calls

@register_button_handler('^open.calls$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(**calls.create_message(context))
