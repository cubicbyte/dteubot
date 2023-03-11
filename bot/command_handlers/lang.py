from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import lang_select, menu

@register_command_handler('lang')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.chat.send_message(**lang_select.create_message(context))
        return

    lang_code = context.args[0].lower()
    context._chat_data.lang_code = lang_code
    await update.message.chat.send_message(**menu.create_message(context))
