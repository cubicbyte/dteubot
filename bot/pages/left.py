import requests.exceptions

from telebot import types
from ..settings import langs
from ..remaining_time_formatted import get_time as get_remaining_time_formatted

def get_text(lang_code: str, groupId: int | None) -> str:
    if groupId is None:
        return langs[lang_code]['text.time.left_unknown']

    try:
        remaining_time = get_remaining_time_formatted(lang_code, groupId)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return langs[lang_code]['text.time.left_unknown']

    if remaining_time['time'] is None or remaining_time['time']['status'] == 3:
        return langs[lang_code]['text.subjects.missing_today']

    if remaining_time['time']['status'] == 1:
        return langs[lang_code]['text.time.left_end'].format(left=remaining_time['formatted'])

    return langs[lang_code]['text.time.left_start'].format(left=remaining_time['formatted'])

def create_message(lang_code: str, groupId: int | None) -> dict:
    left = get_text(lang_code, groupId)
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.refresh'], callback_data='open.left')
    )

    msg = {
        'text': left,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
