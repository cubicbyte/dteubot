import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from . import api_unavaliable, invalid_group
from .. import remaining_time

def create_message(lang_code: str, groupId: int | None) -> dict:
    if groupId is None:
        return invalid_group.create_message(lang_code)

    try:
        rem_time = remaining_time.get_time_formatted(lang_code, groupId)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(lang_code)

    if rem_time['time'] is None or rem_time['time']['status'] == 3:
        page_text = langs[lang_code]['page.left.no_more']
    elif rem_time['time']['status'] == 1:
        page_text = langs[lang_code]['page.left.to_end'].format(left=escape_markdownv2(rem_time['text']))
    else:
        page_text = langs[lang_code]['page.left.to_start'].format(left=escape_markdownv2(rem_time['text']))

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.more'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu')
    )

    msg = {
        'text': page_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
