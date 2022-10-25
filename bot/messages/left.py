from telebot import types
from .. import get_remaining_time_formatted

def create_message(message: types.Message) -> dict:
    remaining_time = get_remaining_time_formatted(message)

    if remaining_time['time'] is None or remaining_time['time']['status'] == 3:
        left = message.lang['text.subjects.missing_today']
    elif remaining_time['time']['status'] == 1:
        left = message.lang['text.time.left_end'].format(left=remaining_time['formatted'])
    else:
        left = message.lang['text.time.left_start'].format(left=remaining_time['formatted'])

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['button.refresh'], callback_data='open.left')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': left,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
