from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import settings


@register_button_handler('^open.settings$')
async def handler(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(
        **settings.create_message(ctx))
    ctx._chat_data.save_message('settings', msg)
