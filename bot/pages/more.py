from functools import cache
from telebot import types
from ..settings import langs

@cache
def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.more']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.calls'], callback_data='open.calls'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.info'], callback_data='open.info')
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
