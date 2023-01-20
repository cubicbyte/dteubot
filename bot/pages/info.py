from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['page.info']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.more'),
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
