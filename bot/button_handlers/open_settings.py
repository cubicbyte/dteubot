from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import settings

@register_button_handler('^open.settings$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(**settings.create_message(context))
