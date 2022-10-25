import requests.exceptions
from telebot import types
from ..settings import api
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command.group']

    try:
        res = api.list_groups(message.config['schedule']['faculty_id'], message.config['schedule']['course'])

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data=f'select.schedule.faculty_id={message.config["schedule"]["faculty_id"]}')
    )

    for group in res.json():
        markup.add(
            types.InlineKeyboardButton(text=group['name'], callback_data=f'select.schedule.group_id={group["id"]}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
