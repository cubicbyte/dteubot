import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from . import api_unavaliable
from ..settings import api

def create_message(context: ContextTypes.DEFAULT_TYPE, structure_id: int) -> dict:
    try:
        faculties = api.list_faculties(structure_id)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(context)

    buttons = [[
        # TODO open structure select page if possible
        InlineKeyboardButton(text=context._chat_data.lang['button.back'], callback_data=f'open.menu')
    ]]

    for faculty in faculties:
        buttons.append([
            InlineKeyboardButton(text=faculty['fullName'], callback_data=f'select.schedule.faculty#structureId={structure_id}&facultyId={faculty["id"]}')
        ])

    return {
        'text': context._chat_data.lang['page.faculty'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
