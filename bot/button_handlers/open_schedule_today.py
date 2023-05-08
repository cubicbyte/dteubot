from datetime import date
from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import schedule
from bot.data import Message


@register_button_handler('^open.schedule.today$')
async def handler(update: Update, context: CallbackContext):
    today = date.today()
    msg = await update.callback_query.edit_message_text(**schedule.create_message(context, date=today))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'left',
                context._chat_data.get('lang_code'),
                {'date': today.strftime('%Y-%m-%d')}))
