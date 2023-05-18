from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import lang_selection


@register_button_handler('^open.select_lang$')
async def handler(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(
        **lang_selection.create_message(ctx))
    ctx._chat_data.save_message('lang_selection', msg)
