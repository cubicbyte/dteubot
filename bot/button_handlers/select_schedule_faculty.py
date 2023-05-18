from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import course_list
from bot.utils import parse_callback_query


@register_button_handler('^select.schedule.faculty')
async def handler(upd: Update, ctx: CallbackContext):
    args = parse_callback_query(upd.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **course_list.create_message(ctx, structure_id, faculty_id))

    # Save message to database
    data = {'structureId': structure_id, 'facultyId': faculty_id}
    ctx._chat_data.save_message('course_list', msg, data)
