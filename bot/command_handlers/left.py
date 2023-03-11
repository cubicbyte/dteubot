from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import left

@register_command_handler('left')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_message(**left.create_message(context))
