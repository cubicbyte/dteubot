from telebot import types
from datetime import timedelta
from .. import get_remaining_time_formatted

def create_message(message: types.Message) -> dict:
    remaining_time = get_remaining_time_formatted(message)

    if remaining_time['time'] is None:
        left = message.lang['text']['subjects_missing_today']
    elif remaining_time['time'] > timedelta(0):
        left = message.lang['text']['ring_left_start'].format(left=remaining_time['formatted'])
    else:
        left = message.lang['text']['ring_left_end'].format(left=remaining_time['formatted'])

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
