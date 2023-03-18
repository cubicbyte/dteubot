from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import lang_selection

@register_button_handler('^open.select_lang$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(**lang_selection.create_message(context))
