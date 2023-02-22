from telebot import types
from ..settings import langs

def create_message(message: types.Message) -> dict:
    message_text = message.lang['page.lang_select'].format(lang=message.lang['lang_name'])
    markup = types.InlineKeyboardMarkup()

    for lang in langs:
        markup.add(
            types.InlineKeyboardButton(text=langs[lang]['lang_name'], callback_data=f'select.lang#lang={lang}')
        )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
