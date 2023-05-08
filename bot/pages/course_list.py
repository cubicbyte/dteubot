import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from settings import api
from bot.pages import api_unavaliable


def create_message(context: ContextTypes.DEFAULT_TYPE, structure_id: int, faculty_id: int) -> dict:
    try:
        courses = api.list_courses(faculty_id)
    except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(context)

    buttons = [[
        InlineKeyboardButton(
            text=context._chat_data.get_lang()['button.back'],
            callback_data=f'select.schedule.structure#structureId={structure_id}')
    ]]

    for course in courses:
        buttons.append([
            InlineKeyboardButton(
                text=str(course.course),
                callback_data=f'select.schedule.course#structureId={structure_id}&facultyId={faculty_id}&course={course.course}')
        ])

    return {
        'text': context._chat_data.get_lang()['page.course'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
