from datetime import timedelta, date as _date
from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import schedule
from ..data import Message

@register_button_handler('^open.schedule.tomorrow$')
async def handler(update: Update, context: CallbackContext):
    date = _date.today() + timedelta(days=1)
    msg = await update.callback_query.edit_message_text(**schedule.create_message(context, date=date))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'left', context._chat_data.get('lang_code'), {'date': date.strftime('%Y-%m-%d')}))
