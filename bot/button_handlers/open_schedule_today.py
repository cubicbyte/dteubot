from datetime import date
from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import schedule

@register_button_handler(r'^open.schedule.today$')
async def handler(update: Update, context: CallbackContext):
    await update.effective_message.edit_text(**schedule.create_message(context, date=date.today()))
