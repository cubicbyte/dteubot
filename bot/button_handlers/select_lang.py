from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import lang_selection, menu
from ..data import Message
from settings import langs, DEFAULT_LANG
from ..utils import parse_callback_query

@register_button_handler('^select.lang')
async def handler(update: Update, context: CallbackContext):
    lang_code = parse_callback_query(update.callback_query.data)['args']['lang']

    if not lang_code in langs:
        lang_code = DEFAULT_LANG

    if lang_code == context._chat_data.get('lang_code'):
        msg = await update.callback_query.edit_message_text(**menu.create_message(context))
        context._chat_data.add_message(Message(msg.message_id, msg.date, 'menu', context._chat_data.get('lang_code')))
        return

    context._chat_data.set('lang_code', lang_code)
    msg = await update.callback_query.edit_message_text(**lang_selection.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'lang_selection', context._chat_data.get('lang_code')))
