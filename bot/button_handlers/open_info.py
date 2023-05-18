from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import info


@register_button_handler('^open.info$')
async def handler(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**info.create_message(ctx))
    ctx._chat_data.save_message('info', msg)
