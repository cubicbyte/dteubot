from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import menu

@register_command_handler('menu')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_message(**menu.create_message(context))
