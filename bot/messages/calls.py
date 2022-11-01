import requests.exceptions
from telebot import types
from ..settings import api
from .api_unavaliable import create_message as create_api_unavaliable_message

def get_text(message: types.Message) -> str:
    msg = ''
    
    try:
        calls = api.timetable_call().json()
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    for call in calls:
        msg += message.lang['text.call_time'].format(**call)

    return msg

def create_message(message: types.Message) -> dict:
    schedule = get_text(message)
    message_text = message.lang['command.calls'].format(schedule=schedule)
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.more'),
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
