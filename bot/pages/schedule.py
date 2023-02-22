import requests.exceptions
import logging

from telebot import types
from datetime import datetime, timedelta, date as _date
from babel.dates import format_date
from ..settings import api
from .invalid_group import create_message as create_invalid_group_message
from .api_unavaliable import create_message as create_api_unavaliable_message
from ..utils.escape_markdown import escape_markdownv2

logger = logging.getLogger()



def count_no_lesson_days(schedule: list[dict[str, any]], date: _date, direction_right = True) -> timedelta | None:
    'Counts the number of days without lessons'
    if not direction_right:
        schedule = reversed(schedule)

    res = None
    for day in schedule:
        day_date = datetime.strptime(day['date'], '%Y-%m-%d').date()
        if direction_right:
            if day_date > date:
                res = day_date - date
                break
        else:
            if day_date < date:
                res = date - day_date
                break

    return res

def get_localized_date(date: _date, message: types.Message) -> str:
    date_localized = escape_markdownv2(format_date(date, locale=message.lang_code))
    week_day_localized = message.lang['text.time.week_day.' + str(date.weekday())]
    full_date_localized = f"*{date_localized}* `[`*{week_day_localized}*`]`"
    return full_date_localized

def create_schedule_section(schedule_day: dict[str, any], message: types.Message) -> str:
    schedule_section = ''
    for lesson in schedule_day['lessons']:
        for period in lesson['periods']:
            # Escape ONLY USED api result not to break telegram markdown
            # DO NOT DELETE COMMENTS
            period['typeStr'] = escape_markdownv2(period['typeStr'])
            period['classroom'] = escape_markdownv2(period['classroom'])
            #period['disciplineFullName'] = escape_markdownv2(period['disciplineFullName'])
            period['disciplineShortName'] = escape_markdownv2(period['disciplineShortName'])
            period['timeStart'] = escape_markdownv2(period['timeStart'])
            period['timeEnd'] = escape_markdownv2(period['timeEnd'])
            #period['teachersName'] = escape_markdownv2(period['teachersName'])
            period['teachersNameFull'] = escape_markdownv2(period['teachersNameFull'])
            #period['dateUpdated'] = escape_markdownv2(period['dateUpdated'])
            #period['groups'] = escape_markdownv2(period['groups'])


            # If there are multiple teachers, display the first one and add +1 to the end
            # TODO: Replace this with textwrap.shorten
            if ',' in period['teachersName']:
                count = str(period['teachersNameFull'].count(','))
                period['teachersName'] = period['teachersName'][:period['teachersName'].index(',')] + ' +' + count
                period['teachersNameFull'] = period['teachersNameFull'][:period['teachersNameFull'].index(',')] + ' +' + count

            schedule_section += message.lang['text.schedule.period'].format(
                **period,
                lessonNumber=lesson['number']
            )

    schedule_section += '`—――—―``―——``―—―``――``—``―``—``――――``――``―――`'
    return schedule_section



def create_message(message: types.Message, date: _date | str) -> dict:
    # Create "date_str" and "date" variables
    if isinstance(date, _date):
        date_str = date.strftime('%Y-%m-%d')
    else:
        date_str = date
        date = datetime.strptime(date, '%Y-%m-%d').date()


    # Get schedule
    dateStart = date - timedelta(days=date.weekday() + 7)
    dateEnd = dateStart + timedelta(days=20)
    try:
        schedule = api.timetable_group(message.config['groupId'], dateStart, dateEnd)
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 422:
            return create_invalid_group_message(message)
        return create_api_unavaliable_message(message)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout
    ):
        return create_api_unavaliable_message(message)


    # Find schedule of current day
    cur_day_schedule = None
    for day in schedule:
        if day['date'] == date_str:
            cur_day_schedule = day
            break


    # Create the schedule page content
    if cur_day_schedule is not None:
        msg_text = message.lang['page.schedule'].format(
            date=get_localized_date(date, message),
            schedule=create_schedule_section(cur_day_schedule, message)
        )
    # If there is no lesson for the current day
    else:
        # Variables with the number of days you need to skip to reach a day with lessons
        skip_left = count_no_lesson_days(schedule, date, direction_right=False)
        skip_right = count_no_lesson_days(schedule, date, direction_right=True)
        if skip_right is None:
            skip_right = dateEnd - date + timedelta(days=1)
        if skip_left is None:
            skip_left = date - dateStart + timedelta(days=1)
        # If there are no lessons for multiple days
        # Then combine all the days without lessons into one page
        if skip_left.days > 1 or skip_right.days > 1:
            dateStart_localized = get_localized_date(date - skip_left + timedelta(days=1), message)
            dateEnd_localized = get_localized_date(date + skip_right - timedelta(days=1), message)
            msg_text = message.lang['page.schedule.empty.multiple_days'].format(
                dateStart=dateStart_localized,
                dateEnd=dateEnd_localized
            )
        # If no lessons for only one day
        else:
            msg_text = message.lang['page.schedule.empty'].format(date=get_localized_date(date, message))



    # Create buttons
    if cur_day_schedule is not None:
        day_next = date + timedelta(days=1)
        day_prev = date - timedelta(days=1)
    else:
        day_next = date + skip_right
        day_prev = date - skip_left
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(text=message.lang['button.navigation.day_previous'], callback_data='open.schedule.day#date=' + day_prev.strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.navigation.day_next'], callback_data='open.schedule.day#date=' + day_next.strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.navigation.week_previous'], callback_data='open.schedule.day#date=' + (date - timedelta(days=7)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.navigation.week_next'], callback_data='open.schedule.day#date=' + (date + timedelta(days=7)).strftime('%Y-%m-%d')),
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu')
    ]
    # If the selected day is not today, then add "today" button
    if date != _date.today():
        buttons.append(types.InlineKeyboardButton(text=message.lang['button.navigation.today'], callback_data='open.schedule.today'))
    markup.add(*buttons)


    msg = {
        'chat_id': message.chat.id,
        'text': msg_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
