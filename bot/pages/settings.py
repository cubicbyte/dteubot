from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from ..settings import api, CachedApi

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    if context._chat_data.group_id is not None:
        if type(api) is CachedApi:
            group = escape_markdown(api._cache.get_group(context._chat_data.group_id)[2], version=2)
        else:
            group = context._chat_data.group_id
    else:
        group = context._chat_data.lang['text.not_selected']

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.lang['button.select_group'], callback_data='open.select_group'),
        InlineKeyboardButton(text=context._chat_data.lang['button.select_lang'], callback_data='open.select_lang')
    ], [
        InlineKeyboardButton(text=context._chat_data.lang['button.back'], callback_data='open.menu')
    ]]

    return {
        'text': context._chat_data.lang['page.settings'].format(group_id=group),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
