from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import schedule
from bot.utils import parse_callback_query


@register_button_handler('^open.schedule.day')
async def handler(upd: Update, ctx: CallbackContext):
    date = parse_callback_query(upd.callback_query.data)['args']['date']
    msg = await upd.callback_query.edit_message_text(
        **schedule.create_message(ctx, date=date))
    ctx._chat_data.save_message('schedule', msg)
