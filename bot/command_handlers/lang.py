from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import lang_select, menu

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        context.bot.send_message(**lang_select.create_message(context), chat_id=update.effective_chat.id)
    else:
        context.chat_data['lang'] = context.args[0]
        context.bot.send_message(**menu.create_message(context), chat_id=update.effective_chat.id)

register_handler(CommandHandler('lang', command_handler))
