from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import greeting, select_structure

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        ref = None
    else:
        ref = context.args[0]

    # TODO: save ref

    context.bot.send_message(**greeting.create_message(context), chat_id=update.effective_chat.id)
    context.bot.send_message(**select_structure.create_message(context), chat_id=update.effective_chat.id)

register_handler(CommandHandler('start', command_handler))
