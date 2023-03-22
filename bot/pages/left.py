import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from . import api_unavaliable, invalid_group
from .. import remaining_time

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    if context._chat_data.get('group_id') is None:
        return invalid_group.create_message(context)

    try:
        rem_time = remaining_time.get_time_formatted(context._chat_data.get('lang_code'), context._chat_data.get('group_id'))
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return api_unavaliable.create_message(context)

    if rem_time['time'] is None or rem_time['time']['status'] == 3:
        page_text = context._chat_data.get_lang()['page.left.no_more']
    elif rem_time['time']['status'] == 1:
        page_text = context._chat_data.get_lang()['page.left.to_end'].format(left=escape_markdown(rem_time['text'], version=2))
    else:
        page_text = context._chat_data.get_lang()['page.left.to_start'].format(left=escape_markdown(rem_time['text'], version=2))

    if rem_time['time'] is None or rem_time['time']['status'] == 3:
        buttons = [[
            InlineKeyboardButton(text=context._chat_data.get_lang()['button.back'], callback_data='open.more'),
            InlineKeyboardButton(text=context._chat_data.get_lang()['button.menu'], callback_data='open.menu')
        ]]
    else:
        buttons = [[
            InlineKeyboardButton(text=context._chat_data.get_lang()['button.menu'], callback_data='open.menu'),
            InlineKeyboardButton(text=context._chat_data.get_lang()['button.refresh'], callback_data='open.left')
        ]]

    return {
        'text': page_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
