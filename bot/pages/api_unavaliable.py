from functools import cache
from telebot import types
from ..settings import langs

@cache
def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.api_unavaliable']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.write_me'], url='https://t.me/cubicbyte')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
