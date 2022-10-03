from telebot import types
from datetime import datetime
from ..get_remaining_time import get_remaining_time

def create_message(message: types.Message) -> dict:
    remaining_time = get_remaining_time(message, datetime.now())

    if remaining_time['to'] == None:
        left = message.lang['text']['subjects_missing_today']

    else:
        remaining = str(remaining_time['remaining'])

        if '.' in remaining:
            remaining = remaining[:remaining.index('.')]

        if remaining_time['to'] == 0:
            left = message.lang['text']['ring_left_start'].format(left=remaining)
        
        elif remaining_time['to'] == 1:
            left = message.lang['text']['ring_left_end'].format(left=remaining)

    message_text = message.lang['command']['menu'].format(left=left)
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_today'], callback_data='open.schedule.today'),
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_tomorrow'], callback_data='open.schedule.tomorrow')
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_settings'], callback_data='open.settings'),
        types.InlineKeyboardButton(text=message.lang['text']['button_refresh'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_more'], callback_data='open.more')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
