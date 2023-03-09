from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import calls

@register_command_handler('calls')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message(**calls.create_message(context))
