from functools import cache
from telebot import types
from ..settings import langs

@cache
def create_message(lang_code: str, groupId: int) -> dict:
    markup = types.InlineKeyboardMarkup()
    message_text = langs[lang_code]['page.settings'].format(group_id=groupId or langs[lang_code]['text.not_selected'])

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
