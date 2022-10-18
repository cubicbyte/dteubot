import requests.exceptions

from telebot import types
from ..settings import chat_configs, api
from .select_faculty import create_message as create_select_faculty_message
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    try:
        structures = api.get_structures().json()

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    if len(structures) == 1:
        message.config['schedule']['structure_id'] = structures[0]['id']
        message._config = chat_configs.set_chat_config_field(message.chat.id, 'schedule', message.config['schedule'])
        return create_select_faculty_message(message)

    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['command']['structure']

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.menu')
    )

    for structure in structures:
        markup.add(
            types.InlineKeyboardButton(text=structure['fullName'], callback_data=f'select.schedule.structure_id={structure["id"]}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
