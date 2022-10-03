import requests.exceptions

from telebot import types
from ..get_groups.src.get_groups import get_groups
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['group']

    try:
        groups = get_groups(message.config['schedule']['faculty_id'], message.config['schedule']['course'], message.config['schedule']['structure_id'])

    except requests.exceptions.ConnectionError:
        return create_api_unavaliable_message(message)

    for group in groups:
        markup.add(
            types.InlineKeyboardButton(text=groups[group], callback_data=f'select.schedule.group_id={group}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
