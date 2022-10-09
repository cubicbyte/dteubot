import requests.exceptions

from telebot import types
from ..get_courses import get_courses
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['course']

    try:
        courses = get_courses(message.config['schedule']['structure_id'], message.config['schedule']['faculty_id']).json()

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data=f'select.schedule.structure_id={message.config["schedule"]["structure_id"]}')
    )

    for course in courses:
        markup.add(
            types.InlineKeyboardButton(text=str(course['course']), callback_data=f'select.schedule.course={course["course"]}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
