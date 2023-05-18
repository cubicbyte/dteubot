from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler


@register_button_handler('^close_page$')
async def handler(upd: Update, ctx: CallbackContext):
    await upd.callback_query.delete_message()
    ctx._chat_data.remove_message(upd.callback_query.message.message_id)
