from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import calls


@register_button_handler('^open.calls$')
async def handler(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**calls.create_message(ctx))
    ctx._chat_data.save_message('calls', msg)
