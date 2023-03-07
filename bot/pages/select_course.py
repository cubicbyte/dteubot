import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from . import api_unavaliable

def create_message(lang_code: str, structureId: int, facultyId: int) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = langs[lang_code]['page.course']

    try:
        res = api.list_courses(facultyId)

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(lang_code)

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data=f'select.schedule.structure#structureId={structureId}')
    )

    for course in res:
        markup.add(
            types.InlineKeyboardButton(text=str(course['course']), callback_data=f'select.schedule.course#structureId={structureId}&facultyId={facultyId}&course={course["course"]}')
        )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
