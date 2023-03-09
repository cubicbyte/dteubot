from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import calls

@register_button_handler(r'^open.calls$')
async def handler(update: Update, context: CallbackContext):
    await update.effective_message.edit_text(**calls.create_message(context))
