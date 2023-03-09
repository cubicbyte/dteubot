from datetime import timedelta, date as _date
from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import schedule

@register_command_handler('tomorrow')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = _date.today() + timedelta(days=1)
    await update.effective_chat.send_message(**schedule.create_message(context, date))
