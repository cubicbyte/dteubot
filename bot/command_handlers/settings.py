from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import settings

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(**settings.create_message(context), chat_id=update.effective_chat.id)

register_handler(CommandHandler('settings', command_handler))
