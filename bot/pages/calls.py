import requests.exceptions

from telebot import types
from ..settings import api, langs
from .api_unavaliable import create_message as create_api_unavaliable_message

def get_text() -> str:
    msg = ''

    for call in api.timetable_call_schedule():
        msg += '`{number})` *{timeStart}* `-` *{timeEnd}*\n'.format(**call)

    return msg

def create_message(lang_code: str) -> dict:
    try:
        schedule = get_text()
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(lang_code)

    message_text = langs[lang_code]['page.calls'].format(schedule=schedule)
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
