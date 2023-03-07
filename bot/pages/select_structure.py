import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from . import api_unavaliable

def create_message(lang_code: str) -> dict:
    try:
        structures = api.list_structures()

    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(lang_code)

    markup = types.InlineKeyboardMarkup()
    message_text = langs[lang_code]['page.structure']

    if len(structures) == 1:
        # If there is only one structure, then skip this menu
        return create_select_faculty_message(lang_code, structures[0]['id'])

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.menu')
    )

    for structure in structures:
        markup.add(
            types.InlineKeyboardButton(text=structure['fullName'], callback_data=f'select.schedule.structure#structureId={structure["id"]}')
        )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
