from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.menu'],
                             callback_data='open.menu')
    ]]

    return {
        'text': context._chat_data.get_lang()['alert.no_permissions'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
