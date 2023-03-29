from telegram import Update
from telegram.ext import ContextTypes
from settings import langs, DEFAULT_LANG
from . import register_command_handler
from ..pages import lang_selection, menu
from ..data import Message

@register_command_handler('lang')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        msg = await update.message.chat.send_message(**lang_selection.create_message(context))
        context._chat_data.add_message(Message(msg.message_id, msg.date, 'lang_selection', context._chat_data.get('lang_code')))
        return

    lang_code = context.args[0].lower()

    if not lang_code in langs:
        lang_code = DEFAULT_LANG

    context._chat_data.set('lang_code', lang_code)
    msg = await update.message.chat.send_message(**menu.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'menu', context._chat_data.get('lang_code')))
