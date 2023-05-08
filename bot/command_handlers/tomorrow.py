from datetime import timedelta, date as _date
from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import schedule
from bot.data import Message


@register_command_handler('tomorrow')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    date = _date.today() + timedelta(days=1)
    msg = await update.message.chat.send_message(**schedule.create_message(context, date))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'schedule',
                context._chat_data.get('lang_code'),
                {'date': date.strftime('%Y-%m-%d')}))
