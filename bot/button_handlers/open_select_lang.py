from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import lang_select

@register_button_handler(r'^open.select_lang$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(**lang_select.create_message(context))
