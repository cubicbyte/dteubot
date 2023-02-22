from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['page.api_unavaliable']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['button.write_me'], url='https://t.me/cubicbyte')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
