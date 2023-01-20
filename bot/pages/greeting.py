from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['page.greeting']

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'parse_mode': 'Markdown'
    }

    return msg
