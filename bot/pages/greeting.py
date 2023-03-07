from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.greeting']

    msg = {
        'text': message_text,
        'parse_mode': 'MarkdownV2'
    }

    return msg
