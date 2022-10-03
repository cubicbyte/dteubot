from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['command']['more']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_info'], callback_data='open.info')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_back'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
