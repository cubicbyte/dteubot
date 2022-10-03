import requests.exceptions
import logging

logger = logging.getLogger()

from telebot import types
from datetime import datetime, timedelta
from ..get_schedule import get_schedule
from . import create_invalid_group_message, create_api_unavaliable_message

def create_message(message: types.Message, date: datetime | str) -> dict:
    if isinstance(date, datetime):
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = date
        date = datetime.strptime(date, '%Y-%m-%d')

    try:
        schedule_res = get_schedule(message, date)
        logger.debug('Parsing schedule')
        schedule = schedule_res.json()

    except requests.exceptions.HTTPError:
        return create_invalid_group_message(message)
    except requests.exceptions.ConnectionError:
        return create_api_unavaliable_message(message)

    schedule_text = ''
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_day_previous'], callback_data='open.schedule.day=' + (date - timedelta(days=1)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_day_next'], callback_data='open.schedule.day=' + (date + timedelta(days=1)).strftime('%Y-%m-%d'))
    )

    markup.add(
        types.InlineKeyboardButton(text=message.lang['text']['button_schedule_today'], callback_data='open.schedule.today')
    )

    day_i = None
    for i in range(len(schedule)):
        if schedule[i]['date'] == date_str:
            day_i = i
            break

    if day_i is None:
        received = message.lang['text']['just_now']
        schedule_text = '\n' + message.lang['text']['no_info']

    else:
        received_date = schedule_res.created_at or datetime.utcnow()
        current_date = datetime.utcnow()
        diff = current_date - received_date
        
        received = '{0} {1} {2}'

        if diff < timedelta(minutes=1):
            received = received.format(int(diff.total_seconds()), message.lang['text']['seconds_short'], message.lang['text']['ago'])
        elif diff < timedelta(hours=1):
            received = received.format(str(diff.seconds // 60), message.lang['text']['minutes_short'], message.lang['text']['ago'])
        elif diff < timedelta(days=1):
            received = received.format(str(diff.seconds // 3600), message.lang['text']['hours_short'], message.lang['text']['ago'])
        else:
            received = received.format(str(diff.days), message.lang['text']['days_short'], message.lang['text']['ago'])

        for lesson in schedule[i]['lessons']:
            for period in lesson['periods']:
                period['teachersName'] = period['teachersName'].replace('`', '\'')
                period['teachersNameFull'] = period['teachersNameFull'].replace('`', '\'')

                lesson_str = message.lang['text']['lesson'].format(
                    **period,
                    number=lesson['number']
                )

                schedule_text += lesson_str

        schedule_text += '\n`—――—―``―——``―—―``――``—``―``—``――――``――``―――`'

    msg_text = message.lang['command']['schedule'].format(
        date=date_str + ' - ' + message.lang['day'][str(date.weekday())],
        schedule=schedule_text,
        received=received
    )

    msg = {
        'chat_id': message.chat.id,
        'text': msg_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
