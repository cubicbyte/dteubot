from functools import lru_cache
from telebot import types
from ..settings import langs

@lru_cache
def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.admin_panel']
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.admin.clear_expired_cache'], callback_data='admin.clear_expired_cache'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.admin.clear_all_cache'], callback_data='admin.clear_all_cache'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.admin.get_logs'], callback_data='admin.get_logs'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.admin.clear_logs'], callback_data='admin.clear_logs'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.back'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
