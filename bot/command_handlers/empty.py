from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import statistic

@register_command_handler(['empty_0', 'empty_1'])
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_message(**statistic.create_message(update, context))
