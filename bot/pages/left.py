import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from bot.pages import api_unavaliable, invalid_group
from bot import remaining_time
from lib.api.exceptions import HTTPApiException


def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    if context._chat_data.get('group_id') is None:
        return invalid_group.create_message(context)

    try:
        rem_time = remaining_time.get_time_formatted(context._chat_data.get('lang_code'),
                                                     context._chat_data.get('group_id'))
    except HTTPApiException:
        return api_unavaliable.create_message(context)

    # Show "no more classes" page
    if rem_time['time'] is None or rem_time['time']['status'] == 3:
        page_text = context._chat_data.get_lang()['page.left.no_more']

    # Show "left to end" page
    elif rem_time['time']['status'] == 1:
        page_text = context._chat_data.get_lang()['page.left.to_end'].format(
            left=escape_markdown(rem_time['text'], version=2))

    # Show "left to start" page
    else:
        page_text = context._chat_data.get_lang()['page.left.to_start'].format(
            left=escape_markdown(rem_time['text'], version=2))

    # Disable "refresh" button if there is no classes
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
