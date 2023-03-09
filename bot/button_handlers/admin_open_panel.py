from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import admin_panel

@register_button_handler(r'^admin.open_panel$')
async def handler(update: Update, context: CallbackContext):
    await update.effective_message.edit_text(**admin_panel.create_message(context))
