import requests.exceptions
import logging
from babel.dates import format_date

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
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    schedule_text = ''
    markup = types.InlineKeyboardMarkup()
    current_date = datetime.today()
    buttons = []

    buttons.append([
        types.InlineKeyboardButton(text=message.lang['text']['button_day_previous'], callback_data='open.schedule.day=' + (date - timedelta(days=1)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['text']['button_menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['text']['button_day_next'], callback_data='open.schedule.day=' + (date + timedelta(days=1)).strftime('%Y-%m-%d'))
    ])

    buttons.append([
        types.InlineKeyboardButton(text=message.lang['text']['button_week_previous'], callback_data='open.schedule.day=' + (date - timedelta(days=7)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['text']['button_week_next'], callback_data='open.schedule.day=' + (date + timedelta(days=7)).strftime('%Y-%m-%d'))
    ])

    if date.date() != current_date.date() or True:
        buttons[1].insert(
            1, types.InlineKeyboardButton(text=message.lang['text']['button_schedule_today'], callback_data='open.schedule.today')
        )

    for button in buttons:
        markup.add(*button)

    day_i = None
    for i in range(len(schedule)):
        if schedule[i]['date'] == date_str:
            day_i = i
            break

    if day_i is None:
        schedule_text = '\n' + message.lang['text']['lesson_empty']

    else:
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

    date_locale = format_date(date, locale=message.lang_code)
    print(date_locale)

    msg_text = message.lang['command']['schedule'].format(
        date=date_locale,
        schedule=schedule_text
    )

    msg = {
        'chat_id': message.chat.id,
        'text': msg_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
