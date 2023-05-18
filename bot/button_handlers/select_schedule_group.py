from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import menu
from bot.utils import parse_callback_query


@register_button_handler('^select.schedule.group')
async def handler(upd: Update, ctx: CallbackContext):
    args = parse_callback_query(upd.callback_query.data)['args']

    group_id = int(args['groupId'])
    ctx._chat_data.set('group_id', group_id)

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **menu.create_message(ctx))

    # Save message to database
    ctx._chat_data.save_message('menu', msg)
