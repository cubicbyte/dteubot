from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import structure_list
from ..data import Message

@register_button_handler('^open.select_group$')
async def handler(update: Update, context: CallbackContext):
    msg = await update.callback_query.edit_message_text(**structure_list.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'structure_list', context._chat_data.get('lang_code')))
