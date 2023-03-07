from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from requests.exceptions import RequestException

def create_message(lang_code: str) -> dict:
    try:
        api_ver = escape_markdownv2(api.version()['name'])
    except RequestException:
        api_ver = langs[lang_code]['text.unknown']

    message_text = langs[lang_code]['page.info'].format(
        api_ver=api_ver,
        api_ver_supported=escape_markdownv2(api.VERSION)
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.more'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
