from telebot import types
from datetime import timedelta
from .. import get_remaining_time_formatted

def create_message(message: types.Message) -> dict:
    remaining_time = get_remaining_time_formatted(message)

    if remaining_time['time'] is None:
        left = message.lang['text.subjects.missing_today']
    elif remaining_time['time'] > timedelta(0):
        left = message.lang['text.time.left_start'].format(left=remaining_time['formatted'])
    else:
        left = message.lang['text.time.left_end'].format(left=remaining_time['formatted'])

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['button.schedule.today'], callback_data='open.schedule.today')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': left,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
