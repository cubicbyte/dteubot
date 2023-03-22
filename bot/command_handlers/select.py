from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import menu, structure_list
from ..data import Message

@register_command_handler('select')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        msg = await update.message.chat.send_message(**structure_list.create_message(context))
        context._chat_data.add_message(Message(msg.message_id, msg.date, 'structure_list', context._chat_data.get('lang_code')))
        return

    group_id = context.args[0]

    if group_id.isnumeric():
        group_id = int(group_id)
        context._chat_data.set('group_id', group_id)

    msg = await update.message.chat.send_message(**menu.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'menu', context._chat_data.get('lang_code')))
