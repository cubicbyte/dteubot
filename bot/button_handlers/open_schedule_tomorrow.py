from datetime import timedelta, date as _date
from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import schedule

@register_button_handler(r'^open.schedule.tomorrow$')
async def handler(update: Update, context: CallbackContext):
    date = _date.today() + timedelta(days=1)
    await update.callback_query.message.edit_text(**schedule.create_message(context, date=date))
