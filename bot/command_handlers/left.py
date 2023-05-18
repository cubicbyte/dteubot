from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import left


@register_command_handler('left')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **left.create_message(ctx))
    ctx._chat_data.save_message('left', msg)
