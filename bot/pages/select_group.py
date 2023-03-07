import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from . import api_unavaliable

def create_message(lang_code: str, structureId: int, facultyId: int, course: int) -> dict:
    try:
        groups = api.list_groups(facultyId, course)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return create_api_unavaliable_message(lang_code)

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data=f'select.schedule.faculty#structureId={structureId}&facultyId={facultyId}')
    )

    buttons = []
    for group in groups:
        buttons.append(
            types.InlineKeyboardButton(text=group['name'], callback_data=f'select.schedule.group#groupId={group["id"]}')
        )
    markup.add(*buttons)

    msg = {
        'text': langs[lang_code]['page.group'],
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
