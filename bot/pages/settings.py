from functools import cache
from telebot import types
from ..settings import langs, api, CachedApi
from ..utils.escape_markdown import escape_markdownv2

@cache
def create_message(lang_code: str, groupId: int) -> dict:
    if groupId is not None:
        if type(api) is CachedApi:
            group = api._cache.get_group(groupId)[2]
        else:
            group = groupId
    else:
        group = langs[lang_code]['text.not_selected']

    message_text = langs[lang_code]['page.settings'].format(group_id=escape_markdownv2(group))
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.select_group'], callback_data='open.select_group'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.select_lang'], callback_data='open.select_lang')
    )

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
