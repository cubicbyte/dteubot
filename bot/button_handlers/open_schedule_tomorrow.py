from datetime import timedelta, date
from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import schedule


@register_button_handler('^open.schedule.tomorrow$')
async def handler(upd: Update, ctx: CallbackContext):
    # Send message
    _date = date.today() + timedelta(days=1)
    msg = await upd.callback_query.edit_message_text(
        **schedule.create_message(ctx, date=_date))
    
    # Save message to database
    data = {'date': _date.strftime('%Y-%m-%d')}
    ctx._chat_data.save_message('schedule', msg, data)
