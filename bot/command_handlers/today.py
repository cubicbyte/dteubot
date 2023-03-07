from datetime import date as _date
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import schedule

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(**schedule.create_message(context, _date.today()), chat_id=update.effective_chat.id)

register_handler(CommandHandler('today', command_handler))
