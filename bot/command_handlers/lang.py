import os
from telegram import Update
from telegram.ext import ContextTypes
from settings import langs
from bot.command_handlers import register_command_handler
from bot.pages import lang_selection, menu


@register_command_handler('lang')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # /lang
    if len(ctx.args) == 0:
        msg = await upd.message.chat.send_message(
            **lang_selection.create_message(ctx))
        ctx._chat_data.save_message('lang_selection', msg)
        return

    # /lang <lang_code>
    lang_code = ctx.args[0].lower()

    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')

    ctx._chat_data.set('lang_code', lang_code)

    msg = await upd.message.chat.send_message(
        **menu.create_message(ctx))
    ctx._chat_data.save_message('menu', msg)
