from functools import cache
from telebot import types
from ..settings import langs

@cache
def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.lang_select'].format(lang=langs[lang_code]['lang_name'])
    markup = types.InlineKeyboardMarkup()

    for lang in langs:
        markup.add(
            types.InlineKeyboardButton(text=langs[lang]['lang_name'], callback_data=f'select.lang#lang={lang}')
        )

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
