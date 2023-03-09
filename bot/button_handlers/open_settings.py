from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import settings

@register_button_handler(r'^open.settings$')
async def handler(update: Update, context: CallbackContext):
    await update.effective_message.edit_text(**settings.create_message(context))
