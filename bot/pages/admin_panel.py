from telebot import types

def create_message(message: types.Message) -> dict:
    message_text = message.lang['page.admin_panel']
    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.admin.clear_expired_cache'], callback_data='admin.clear_expired_cache'),
        types.InlineKeyboardButton(text=message.lang['button.admin.clear_all_cache'], callback_data='admin.clear_all_cache'),
        types.InlineKeyboardButton(text=message.lang['button.admin.get_logs'], callback_data='admin.get_logs'),
        types.InlineKeyboardButton(text=message.lang['button.admin.clear_logs'], callback_data='admin.clear_logs'),
        types.InlineKeyboardButton(text=message.lang['button.back'], callback_data='open.menu')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
