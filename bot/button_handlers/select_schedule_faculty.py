from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import select_course
from ..utils import parse_callback_query

@register_button_handler(r'^select.schedule.faculty')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']
    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    await update.callback_query.message.edit_text(**select_course.create_message(context, structure_id, faculty_id))
