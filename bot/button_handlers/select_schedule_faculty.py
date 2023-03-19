from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import course_list
from ..utils import parse_callback_query

@register_button_handler('^select.schedule.faculty')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']
    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    await update.callback_query.edit_message_text(**course_list.create_message(context, structure_id, faculty_id))
