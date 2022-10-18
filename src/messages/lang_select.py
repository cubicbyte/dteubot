from telebot import types
from ..settings import langs

def create_message(message: types.Message) -> dict:
    markup = types.InlineKeyboardMarkup()

    if message.config['lang'] == None:
        chat_lang = message.lang['text']['not_selected']
    else:
        chat_lang = langs[message.config['lang']]['lang_name']

    message_text = message.lang['command']['lang_select'].format(lang=chat_lang)

    for lang in langs:
        markup.add(
            types.InlineKeyboardButton(text=langs[lang]['lang_name'], callback_data=f'select.lang={lang}')
        )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
