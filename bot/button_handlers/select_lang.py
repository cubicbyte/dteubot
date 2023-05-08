from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import lang_selection, menu
from bot.data import Message
from bot.utils import parse_callback_query
from settings import langs, DEFAULT_LANG


@register_button_handler('^select.lang')
async def handler(update: Update, context: CallbackContext):
    lang_code = parse_callback_query(update.callback_query.data)['args']['lang']

    if not lang_code in langs:
        lang_code = DEFAULT_LANG

    # Open menu if user selected the same language
    if lang_code == context._chat_data.get('lang_code'):
        msg = await update.callback_query.edit_message_text(**menu.create_message(context))
        context._chat_data.add_message(
            Message(msg.message_id, msg.date, 'menu', context._chat_data.get('lang_code')))
        return

    # Update language and refresh page
    context._chat_data.set('lang_code', lang_code)
    msg = await update.callback_query.edit_message_text(**lang_selection.create_message(context))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'lang_selection', context._chat_data.get('lang_code')))
