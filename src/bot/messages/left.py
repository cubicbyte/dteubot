import requests.exceptions
from telebot import types
from .. import get_remaining_time_formatted

def get_text(message: types.Message) -> str:
    if message.config['groupId'] is None:
        return message.lang['text.time.left_unknown']

    try:
        remaining_time = get_remaining_time_formatted(message)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return message.lang['text.time.left_unknown']

    if remaining_time['time'] is None or remaining_time['time']['status'] == 3:
        return message.lang['text.subjects.missing_today']

    if remaining_time['time']['status'] == 1:
        return message.lang['text.time.left_end'].format(left=remaining_time['formatted'])

    return message.lang['text.time.left_start'].format(left=remaining_time['formatted'])

def create_message(message: types.Message) -> dict:
    left = get_text(message)
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
