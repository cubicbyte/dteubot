from datetime import date
from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import schedule


@register_command_handler('today')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Send message
    _date = date.today()
    msg = await upd.message.chat.send_message(
        **schedule.create_message(ctx, _date))

    # Save message
    data = {'date': _date.strftime('%Y-%m-%d')}
    ctx._chat_data.save_message('schedule', msg, data)
