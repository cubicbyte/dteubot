from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import menu, structure_list

@register_command_handler('select')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.chat.send_message(**structure_list.create_message(context))
        return

    group_id = context.args[0]

    if group_id.isnumeric():
        group_id = int(group_id)
        context._chat_data.group_id = group_id

    await update.message.chat.send_message(**menu.create_message(context))
