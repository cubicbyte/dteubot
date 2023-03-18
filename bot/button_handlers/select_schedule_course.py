from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import group_list
from ..utils import parse_callback_query

@register_button_handler('^select.schedule.course')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']
    structure_id = int(args['structureId'])
    faculty_id = int(args['facultyId'])
    course = int(args['course'])
    await update.callback_query.message.edit_text(**group_list.create_message(context, structure_id, faculty_id, course))
