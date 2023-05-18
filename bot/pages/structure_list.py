import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from settings import api
from bot.pages import api_unavaliable, faculty_list
from lib.api.exceptions import HTTPApiException


def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    try:
        structures = api.list_structures()
    except HTTPApiException:
        return api_unavaliable.create_message(context)

    # If there is only one structure, show faculties page
    if len(structures) == 1:
        return faculty_list.create_message(context, structures[0].id)

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.back'], callback_data=f'open.menu')
    ]]

    for structure in structures:
        buttons.append([
            InlineKeyboardButton(text=structure.fullName,
                                 callback_data=f'select.schedule.structure#structureId={structure.id}')
        ])

    return {
        'text': context._chat_data.get_lang()['page.structure'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
