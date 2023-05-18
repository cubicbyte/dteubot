from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import group_list
from bot.utils import parse_callback_query


@register_button_handler('^select.schedule.course')
async def handler(upd: Update, ctx: CallbackContext):
    args = parse_callback_query(upd.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    course = int(args['course'])

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **group_list.create_message(ctx, structure_id, faculty_id, course))

    # Save message to database
    data = {'structureId': structure_id,
            'facultyId': faculty_id, 'course': course}
    ctx._chat_data.save_message('group_list', msg, data)
