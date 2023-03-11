from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import settings

@register_command_handler('settings')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_message(**settings.create_message(context))
