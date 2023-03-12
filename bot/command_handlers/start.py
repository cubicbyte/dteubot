from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import greeting, structure_list

@register_command_handler('start')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        ref = None
    else:
        ref = context.args[0]

    if context._user_data.ref is None:
        context._user_data.ref = ref

    await update.message.chat.send_message(**greeting.create_message(context))
    await update.message.chat.send_message(**structure_list.create_message(context))
