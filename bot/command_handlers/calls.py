from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import calls
from ..data import Message

@register_command_handler('calls')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.chat.send_message(**calls.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'calls', context._chat_data.get('lang_code')))
