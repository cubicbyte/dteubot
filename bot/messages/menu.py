from telebot import types
from .left import get_text as get_remaining_time_text

def create_message(message: types.Message) -> dict:
    left = get_remaining_time_text(message)
    message_text = message.lang['command.menu'].format(left=left)
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.schedule.today'], callback_data='open.schedule.today'),
        types.InlineKeyboardButton(text=message.lang['button.schedule.tomorrow'], callback_data='open.schedule.tomorrow')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.settings'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['button.refresh'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['button.more'], callback_data='open.more')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }
 
    return msg
