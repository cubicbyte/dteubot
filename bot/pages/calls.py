import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from ..pages import api_unavaliable
from ..settings import api

def get_schedule_section_text() -> str:
    text = ''
    for call in api.timetable_call_schedule():
        text += '`{number})` *{timeStart}* `-` *{timeEnd}*\n'.format(**call)
    return text

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    try:
        schedule_section = get_schedule_section_text()
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(context)

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.lang['button.back'], callback_data='open.more'),
        InlineKeyboardButton(text=context._chat_data.lang['button.menu'], callback_data='open.menu')
    ]]

    return {
        'text': context._chat_data.lang['page.calls'].format(schedule=schedule_section),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
