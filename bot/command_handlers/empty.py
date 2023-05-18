from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import statistic


@register_command_handler(['empty_0', 'empty_1'])
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = await upd.message.chat.send_message(
        **statistic.create_message(upd, ctx))
    ctx._chat_data.save_message('statistic', msg)
