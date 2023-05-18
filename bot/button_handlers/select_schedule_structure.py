from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import faculty_list
from bot.utils import parse_callback_query


@register_button_handler('^select.schedule.structure')
async def handler(upd: Update, ctx: CallbackContext):
    args = parse_callback_query(upd.callback_query.data)['args']

    structure_id = int(args['structureId'])

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **faculty_list.create_message(ctx, structure_id))

    # Save message to database
    data = {'structureId': structure_id}
    ctx._chat_data.save_message('faculty_list', msg, data)
