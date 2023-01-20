from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['page.menu']
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.schedule'], callback_data='open.schedule.today')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.settings'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['button.more'], callback_data='open.more')
    )

    # If user is admin, then add control panel button
    if message.config['admin'] is True:
        markup.add(
            types.InlineKeyboardButton(text=message.lang['button.admin.panel'], callback_data='admin.open_panel')
        )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
