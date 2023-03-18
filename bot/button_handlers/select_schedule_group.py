from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import menu
from ..utils import parse_callback_query

@register_button_handler('^select.schedule.group')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']
    group_id = int(args['groupId'])
    context._chat_data.group_id = group_id
    await update.callback_query.message.edit_text(**menu.create_message(context))
