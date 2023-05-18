from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import greeting, structure_list


@register_command_handler('start')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Get referral code
    if len(ctx.args) == 0:
        ref = None
    else:
        ref = ctx.args[0]

    # Set referral code
    if ctx._user_data.get('ref') is None:
        ctx._user_data.set('ref', ref)

    # Send greeting message
    msg = await upd.message.chat.send_message(
        **greeting.create_message(ctx))
    ctx._chat_data.save_message('greeting', msg)

    # Send main message
    msg = await upd.message.chat.send_message(
        **structure_list.create_message(ctx))
    ctx._chat_data.save_message('structure_list', msg)
