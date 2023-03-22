from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import schedule
from ..utils import parse_callback_query
from ..data import Message

@register_button_handler('^open.schedule.day')
async def handler(update: Update, context: CallbackContext):
    date = parse_callback_query(update.callback_query.data)['args']['date']
    msg = await update.callback_query.edit_message_text(**schedule.create_message(context, date=date))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'schedule', context._chat_data.get('lang_code'), {'date': date}))
