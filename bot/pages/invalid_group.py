from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.invalid_group']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=langs[lang_code]['button.select_group'], callback_data='open.select_group'),
        types.InlineKeyboardButton(text=langs[lang_code]['button.menu'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
