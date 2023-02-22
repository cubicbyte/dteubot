import requests.exceptions

from telebot import types
from ..settings import api, langs
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(lang_code: str, structureId: int) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = langs[lang_code]['page.faculty']

    try:
        res = api.list_faculties(structureId)

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(lang_code)

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.menu')
    )

    for faculty in res:
        markup.add(
            types.InlineKeyboardButton(text=faculty['fullName'], callback_data=f'select.schedule.faculty#structureId={structureId}&facultyId={faculty["id"]}')
        )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
