from telegram import Update
from telegram.ext import ContextTypes
from . import register_command_handler
from ..pages import left
from ..data import Message

@register_command_handler('left')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.chat.send_message(**left.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'left', context._chat_data.get('lang_code')))
