from datetime import date as _date
from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import schedule

@register_command_handler('today')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_message(**schedule.create_message(context, _date.today()))
