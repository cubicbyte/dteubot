import requests.exceptions

from telebot import types
from ..get_faculties.src.get_faculties import get_faculties
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['faculty']

    try:
        faculties = get_faculties(message.config['schedule']['structure_id'])

    except requests.exceptions.ConnectionError:
        return create_api_unavaliable_message(message)

    for faculty in faculties:
        markup.add(
            types.InlineKeyboardButton(text=faculties[faculty], callback_data=f'select.schedule.faculty_id={faculty}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
