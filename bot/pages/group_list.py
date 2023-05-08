import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from settings import api
from bot.pages import api_unavaliable
from bot.utils import array_split


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
        InlineKeyboardButton(
            text=context._chat_data.get_lang()['button.back'],
            callback_data=f'select.schedule.faculty#structureId={structure_id}&facultyId={faculty_id}')
    ]]

    group_btns = []
    for group in groups:
        group_btns.append(
            InlineKeyboardButton(
                text=group.name,
                callback_data=f'select.schedule.group#groupId={group.id}')
        )

    # Make many 3-wide button rows like this: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    buttons.extend(array_split(group_btns, 3))

    return {
        'text': context._chat_data.get_lang()['page.group'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
