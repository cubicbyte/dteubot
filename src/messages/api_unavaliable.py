from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['command']['api_unavaliable']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_write_me'], url='https://t.me/Bogdan4igg')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
