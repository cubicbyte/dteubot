import requests.exceptions
from telebot import types
from ..settings import api
from .select_faculty import create_message as create_select_faculty_message
from .api_unavaliable import create_message as create_api_unavaliable_message

def create_message(message: types.Message) -> dict:
    try:
        structures = api.list_structures()

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(message)

    markup = types.InlineKeyboardMarkup()
    message_text = message.lang['page.structure']

    if len(structures) == 1:
        # If there is only one structure, then skip this menu
        return create_select_faculty_message(message, structures[0]['id'])

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.menu')
    )

    for structure in structures:
        markup.add(
            types.InlineKeyboardButton(text=structure['fullName'], callback_data=f'select.schedule.structure#structureId={structure["id"]}')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
