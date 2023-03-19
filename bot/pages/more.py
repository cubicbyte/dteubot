from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.calls'], callback_data='open.calls'),
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.left'], callback_data='open.left')
    ], [
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.info'], callback_data='open.info')
    ], [
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.back'], callback_data='open.menu')
    ]]

    return {
        'text': context._chat_data.get_lang()['page.more'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
