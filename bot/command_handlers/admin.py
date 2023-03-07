from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import admin_panel, access_denied

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('admin') is not True:
        context.bot.send_message(**access_denied.create_message(context), chat_id=update.effective_chat.id)
        return

    context.bot.send_message(**admin_panel.create_message(context), chat_id=update.effective_chat.id)

register_handler(CommandHandler('admin', command_handler))
