import requests.exceptions
from telebot import types
from ..settings import api
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message, structureId: int, facultyId: int) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['page.course']

    try:
        res = api.list_courses(facultyId)

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(message)

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data=f'select.schedule.structure#structureId={structureId}')
    )

    for course in res:
        markup.add(
            types.InlineKeyboardButton(text=str(course['course']), callback_data=f'select.schedule.course#structureId={structureId}&facultyId={facultyId}&course={course["course"]}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
