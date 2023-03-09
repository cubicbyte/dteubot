import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from . import api_unavaliable
from ..settings import api
from ..utils.array_split import array_split

def create_message(context: ContextTypes.DEFAULT_TYPE, structure_id: int, faculty_id: int, course: int) -> dict:
    try:
        groups = api.list_groups(faculty_id, course)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(context)

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.lang['button.back'], callback_data=f'select.schedule.faculty#structureId={structure_id}&facultyId={faculty_id}')
    ]]

    group_btns = []
    for group in groups:
        group_btns.append(
            InlineKeyboardButton(text=group['name'], callback_data=f'select.schedule.group#groupId={group["id"]}')
        )

    buttons.extend(array_split(group_btns, 3))

    return {
        'text': context._chat_data.lang['page.group'],
        'reply_markup': InlineKeyboardMarkup(buttons, ),
        'parse_mode': 'MarkdownV2'
    }
