from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes


def create_message(context: ContextTypes) -> dict:
    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.menu'],
                             callback_data='open.menu'),
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.write_me'],
                             url='https://t.me/cubicbyte')
    ]]

    return {
        'text': context._chat_data.get_lang()['page.api_unavaliable'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
