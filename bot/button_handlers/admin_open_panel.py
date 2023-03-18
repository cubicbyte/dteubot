from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler, validate_admin
from ..pages import admin_panel

@register_button_handler('^admin.open_panel$')
@validate_admin
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text(**admin_panel.create_message(context))
