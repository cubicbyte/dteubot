from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import calls

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(**calls.create_message(context), chat_id=update.effective_chat.id)

register_handler(CommandHandler('calls', command_handler))
