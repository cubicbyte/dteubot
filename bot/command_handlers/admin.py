from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import admin_panel, access_denied

@register_command_handler('admin')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('admin') is not True:
        await update.effective_chat.send_message(**access_denied.create_message(context))
        return

    await update.effective_chat.send_message(**admin_panel.create_message(context))
