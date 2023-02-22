from functools import lru_cache
from telebot import types
from ..settings import langs

@lru_cache
def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.info']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.more'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
