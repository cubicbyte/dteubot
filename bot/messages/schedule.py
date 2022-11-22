import requests.exceptions
import logging

from telebot import types
from datetime import datetime, timedelta
from babel.dates import format_date
from ..settings import api
from .invalid_group import create_message as create_invalid_group_message
from .api_unavaliable import create_message as create_api_unavaliable_message

logger = logging.getLogger()

def create_lessons_empty_text(message: types.Message) -> str:
    line = '—————————————————————————'
    lessons_missing_text = message.lang['text.subjects.missing']
    spaces_count = int(len(line) / 2) - int(len(lessons_missing_text) / 2)
    
    # All this code is needed to center the text
    if spaces_count < 0:
        spaces_count = 0
    elif len(line) % 2 == 0 and len(lessons_missing_text) % 2 != 0:
        spaces_count -= 1

    spaces = ' ' * spaces_count
    text = f"`{line}`\n\n`{spaces}``{lessons_missing_text}`\n\n`{line}`"

    return text

def create_message(message: types.Message, date: datetime | str) -> dict:
    if isinstance(date, datetime):
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = date
        date = datetime.strptime(date, '%Y-%m-%d')

    try:
        res = api.timetable_group(message.config['groupId'], date)
        if res.status_code == 422:
            return create_invalid_group_message(message)

    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return create_api_unavaliable_message(message)

    schedule = res.json()
    schedule_text = ''
    markup = types.InlineKeyboardMarkup()
    current_date = datetime.today()

    buttons = [[
        types.InlineKeyboardButton(text=message.lang['button.navigation.day_previous'], callback_data='open.schedule.day#date=' + (date - timedelta(days=1)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.navigation.day_next'], callback_data='open.schedule.day#date=' + (date + timedelta(days=1)).strftime('%Y-%m-%d'))
    ], [
        types.InlineKeyboardButton(text=message.lang['button.navigation.week_previous'], callback_data='open.schedule.day#date=' + (date - timedelta(days=7)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text=message.lang['button.navigation.week_next'], callback_data='open.schedule.day#date=' + (date + timedelta(days=7)).strftime('%Y-%m-%d'))
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
        schedule_text = create_lessons_empty_text(message)

    else:
        # Make schedule page content
        for lesson in schedule[i]['lessons']:
            for period in lesson['periods']:
                period['teachersName'] = period['teachersName'].replace('`', '\'')
                period['teachersNameFull'] = period['teachersNameFull'].replace('`', '\'')
                
                # If there are multiple teachers, display the first one and add +1 to the end
                if ',' in period['teachersName']:
                    count = str(period['teachersNameFull'].count(','))
                    period['teachersName'] = period['teachersName'][:period['teachersName'].index(',')] + ' +' + count
                    period['teachersNameFull'] = period['teachersNameFull'][:period['teachersNameFull'].index(',')] + ' +' + count

                schedule_text += f"`———— ``{period['timeStart']}`` ——— ``{period['timeEnd']}`` ————`\n"
                schedule_text += f"`  `*{period['disciplineShortName']}*`[{period['typeStr']}]`\n"
                schedule_text += f"`{lesson['number']} `{period['classroom']}\n`  `{period['teachersNameFull']}\n"

        schedule_text += '`—――—―``―——``―—―``――``—``―``—``――――``――``―――`'


    date_locale = format_date(date, locale=message.lang_code)
    week_day_locale = message.lang['text.time.week_day.' + str(date.weekday())]
    full_date_locale = f"*{date_locale}* `[`*{week_day_locale}*`]`"

    msg_text = message.lang['command.schedule'].format(
        date=full_date_locale,
        schedule=schedule_text
    )

    if res.is_expired:
        msg_text += '\n\n' + message.lang['text.from_cache']

    msg = {
        'chat_id': message.chat.id,
        'text': msg_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
