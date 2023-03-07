from datetime import timedelta, date as _date
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import schedule

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = _date.today() + timedelta(days=1)
    context.bot.send_message(**schedule.create_message(context, date), chat_id=update.effective_chat.id)

register_handler(CommandHandler('tomorrow', command_handler))
