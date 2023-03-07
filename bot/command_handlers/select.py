from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from . import register_handler
from ..pages import menu, select_structure

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        context.bot.send_message(**select_structure.create_message(context), chat_id=update.effective_chat.id)
    else:
        group_id = context.args[0]

        if group_id.isnumeric():
            group_id = int(group_id)
            context.chat_data['groupId'] = group_id

        context.bot.send_message(**menu.create_message(context), chat_id=update.effective_chat.id)

register_handler(CommandHandler('select', command_handler))
