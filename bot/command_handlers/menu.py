from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import menu


@register_command_handler('menu')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **menu.create_message(ctx))
    ctx._chat_data.save_message('menu', msg)
