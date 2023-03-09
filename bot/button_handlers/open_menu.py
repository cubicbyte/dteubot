from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import menu

@register_button_handler(r'^open.menu$')
async def handler(update: Update, context: CallbackContext):
    await update.effective_message.edit_text(**menu.create_message(context))
