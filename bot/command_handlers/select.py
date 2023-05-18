from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import menu, structure_list


@register_command_handler('select')
async def handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # /select
    if len(ctx.args) == 0:
        msg = await upd.message.chat.send_message(
            **structure_list.create_message(ctx))
        ctx._chat_data.save_message('structure_list', msg)
        return

    # /select <group_id>
    group_id = ctx.args[0]

    # Check if group_id is number
    if group_id.isnumeric():
        group_id = int(group_id)
        ctx._chat_data.set('group_id', group_id)
    else:
        # TODO: send error message
        pass

    msg = await upd.message.chat.send_message(
        **menu.create_message(ctx))
    ctx._chat_data.save_message('menu', msg)
