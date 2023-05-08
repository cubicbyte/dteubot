from datetime import date as _date
from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import schedule
from bot.data import Message


@register_command_handler('today')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = _date.today()
    msg = await update.message.chat.send_message(**schedule.create_message(context, today))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'schedule',
                context._chat_data.get('lang_code'),
                {'date': today.strftime('%Y-%m-%d')}))
