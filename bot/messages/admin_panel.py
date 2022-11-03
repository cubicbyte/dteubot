from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['command.admin_panel']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.clear_expired_cache'], callback_data='admin.clear_expired_cache')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.clear_all_cache'], callback_data='admin.clear_all_cache')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
