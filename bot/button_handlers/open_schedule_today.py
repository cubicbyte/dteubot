from datetime import date
from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import schedule

@register_button_handler('^open.schedule.today$')
async def handler(update: Update, context: CallbackContext):
    await update.callback_query.edit_message_text(**schedule.create_message(context, date=date.today()))
