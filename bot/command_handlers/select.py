from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import menu, structure_list
from bot.data import Message


@register_command_handler('select')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /select
    if len(context.args) == 0:
        msg = await update.message.chat.send_message(**structure_list.create_message(context))
        context._chat_data.add_message(
            Message(msg.message_id, msg.date, 'structure_list', context._chat_data.get('lang_code')))
        return

    # /select <group_id>
    group_id = context.args[0]

    if group_id.isnumeric():
        group_id = int(group_id)
        context._chat_data.set('group_id', group_id)
    else:
        # TODO: send error message
        pass

    msg = await update.message.chat.send_message(**menu.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'menu', context._chat_data.get('lang_code')))
