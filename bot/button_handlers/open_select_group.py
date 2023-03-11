from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import select_structure

@register_button_handler(r'^open.select_group$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(**select_structure.create_message(context))
