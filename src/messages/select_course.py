import requests.exceptions

from telebot import types
from ..get_courses.src.get_courses import get_courses
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['course']

    try:
        courses = get_courses(message.config['schedule']['faculty_id'], message.config['schedule']['structure_id'])

    except requests.exceptions.ConnectionError:
        return create_api_unavaliable_message(message)

    for course in courses:
        markup.add(
            types.InlineKeyboardButton(text=courses[course], callback_data=f'select.schedule.course={course}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
