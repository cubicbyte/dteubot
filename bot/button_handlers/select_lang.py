import os
from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import lang_selection, menu
from bot.utils import parse_callback_query
from settings import langs


@register_button_handler('^select.lang')
async def handler(upd: Update, ctx: CallbackContext):
    lang_code = parse_callback_query(upd.callback_query.data)['args']['lang']

    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')

    # Open menu if user selected the same language
    if lang_code == ctx._chat_data.get('lang_code'):
        msg = await upd.callback_query.edit_message_text(
            **menu.create_message(ctx))
        ctx._chat_data.save_message('menu', msg)
        return

    # Update language and refresh page
    ctx._chat_data.set('lang_code', lang_code)
    msg = await upd.callback_query.edit_message_text(
        **lang_selection.create_message(ctx))
    ctx._chat_data.save_message('lang_selection', msg)
