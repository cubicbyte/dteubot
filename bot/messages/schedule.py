import requests.exceptions
import logging

from telebot import types
from datetime import datetime, timedelta
from babel.dates import format_date
from ..settings import api
from .invalid_group import create_message as create_invalid_group_message
from .api_unavaliable import create_message as create_api_unavaliable_message

logger = logging.getLogger()

def create_message(message: types.Message, date: datetime | str) -> dict:
    if isinstance(date, datetime):
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = date
        date = datetime.strptime(date, '%Y-%m-%d')

    try:
        res = api.timetable_group(message.config['schedule']['group_id'], date)
        if res.status_code == 422:
            return create_invalid_group_message(message)

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    schedule = res.json()
    schedule_text = ''
    markup = types.InlineKeyboardMarkup()
    current_date = datetime.today()

    buttons = [[
        types.InlineKeyboardButton(text=message.lang['button.navigation.day_previous'], callback_data='open.schedule.day=' + (date - timedelta(days=1)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.navigation.day_next'], callback_data='open.schedule.day=' + (date + timedelta(days=1)).strftime('%Y-%m-%d'))
    ], [
        types.InlineKeyboardButton(text=message.lang['button.navigation.week_previous'], callback_data='open.schedule.day=' + (date - timedelta(days=7)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['button.navigation.week_next'], callback_data='open.schedule.day=' + (date + timedelta(days=7)).strftime('%Y-%m-%d'))
    ]]

    if date.date() != current_date.date():
        # If the selected day is not today, then add "today" button
        buttons[0].insert(
            1, types.InlineKeyboardButton(text=message.lang['button.navigation.today'], callback_data='open.schedule.today')
        )

    for button in buttons:
        markup.add(*button)

    # Find day in schedule
    day_i = None
    for i in range(len(schedule)):
        if schedule[i]['date'] == date_str:
            day_i = i
            break
    if day_i is None:
        schedule_text = '\n' + message.lang['text.lesson_empty']

    else:
        # Make schedule page content
        for lesson in schedule[i]['lessons']:
            for period in lesson['periods']:
                period['teachersName'] = period['teachersName'].replace('`', '\'')
                period['teachersNameFull'] = period['teachersNameFull'].replace('`', '\'')
                
                if ',' in period['teachersName']:
                    count = str(period['teachersNameFull'].count(','))
                    period['teachersName'] = period['teachersName'][:period['teachersName'].index(',')] + ' +' + count
                    period['teachersNameFull'] = period['teachersNameFull'][:period['teachersNameFull'].index(',')] + ' +' + count

                lesson_str = message.lang['text.lesson'].format(
                    **period,
                    number=lesson['number']
                )

                schedule_text += lesson_str

        schedule_text += '\n`—――—―``―——``―—―``――``—``―``—``――――``――``―――`'

    date_locale = format_date(date, locale=message.lang_code)

    msg_text = message.lang['command.schedule'].format(
        date=date_locale,
        day=message.lang['text.time.week_day.short.' + str(date.weekday())],
        schedule=schedule_text
    )

    msg = {
        'chat_id': message.chat.id,
        'text': msg_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
