from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import faculty_list
from ..utils import parse_callback_query

@register_button_handler('^select.schedule.structure')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']
    structure_id = int(args['structureId'])
    await update.callback_query.message.edit_text(**faculty_list.create_message(context, structure_id))
