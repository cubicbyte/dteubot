from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import settings


@register_command_handler('settings')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **settings.create_message(ctx))
    ctx._chat_data.save_message('settings', msg)
