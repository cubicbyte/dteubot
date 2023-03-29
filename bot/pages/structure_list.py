import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from settings import api
from . import api_unavaliable, faculty_list

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    try:
        structures = api.list_structures()
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(context)

    if len(structures) == 1:
        return faculty_list.create_message(context, structures[0].id)

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.back'], callback_data=f'open.menu')
    ]]

    for structure in structures:
        buttons.append([
            InlineKeyboardButton(text=structure.fullName, callback_data=f'select.schedule.structure#structureId={structure.id}')
        ])

    return {
        'text': context._chat_data.get_lang()['page.structure'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
