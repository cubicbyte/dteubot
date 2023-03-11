from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from requests.exceptions import RequestException
from ..settings import api

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    try:
        api_ver = escape_markdown(api.version()['name'], version=2)
    except RequestException:
        api_ver = context._chat_data.lang['text.unknown']

    message_text = context._chat_data.lang['page.info'].format(
        api_ver=api_ver,
        api_ver_supported=escape_markdown(api.VERSION, version=2)
    )

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.lang['button.back'], callback_data='open.more'),
        InlineKeyboardButton(text=context._chat_data.lang['button.menu'], callback_data='open.menu')
    ]]

    return {
        'text': message_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
