from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import group_list
from bot.utils import parse_callback_query
from bot.data import Message


@register_button_handler('^select.schedule.course')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']

    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    course = int(args['course'])

    msg = await update.callback_query.edit_message_text(
        **group_list.create_message(context, structure_id, faculty_id, course))

    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'group_list',
                context._chat_data.get('lang_code'),
                {'structureId': structure_id, 'facultyId': faculty_id, 'course': course}))
