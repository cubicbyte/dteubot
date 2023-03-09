from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    buttons = []

    for i in context.bot_data.langs:
        buttons.append([
            InlineKeyboardButton(text=context.bot_data.langs[i]['lang_name'], callback_data=f'select.lang#lang={i}')
        ])

    buttons.append([
        InlineKeyboardButton(text=context._chat_data.lang['button.back'], callback_data='open.settings'),
        InlineKeyboardButton(text=context._chat_data.lang['button.menu'], callback_data='open.menu')
    ])

    return {
        'text': context._chat_data.lang['page.lang_select'].format(lang=context._chat_data.lang['lang_name']),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
