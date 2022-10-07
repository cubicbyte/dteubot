from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['text']['group_incorrect']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_select_group'], callback_data='open.select_group'),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
