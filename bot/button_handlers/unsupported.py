from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import menu

# TODO move this to main.py file
@register_button_handler()
async def handler(update: Update, context: CallbackContext):
    # TODO add dedicated page here
    await update.effective_message.edit_text(**menu.create_message(context))
