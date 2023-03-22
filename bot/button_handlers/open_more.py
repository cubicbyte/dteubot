from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import more
from ..data import Message

@register_button_handler('^open.more$')
async def handler(update: Update, context: CallbackContext):
    msg = await update.callback_query.edit_message_text(**more.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'more', context._chat_data.get('lang_code')))
