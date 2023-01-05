import requests.exceptions
from telebot import types
from ..settings import api
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message, structureId: int) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command.faculty']

    try:
        res = api.list_faculties(structureId)

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(message)

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.menu')
    )

    for faculty in res.json():
        markup.add(
            types.InlineKeyboardButton(text=faculty['fullName'], callback_data=f'select.schedule.faculty#structureId={structureId}&facultyId={faculty["id"]}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
