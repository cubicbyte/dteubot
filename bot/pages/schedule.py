import requests.exceptions
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from datetime import datetime, timedelta, date as _date
from babel.dates import format_date
from lib.api.schemas import TimeTableDate
from . import invalid_group, api_unavaliable
from ..settings import api
from ..utils import array_split



def count_no_lesson_days(schedule: list[TimeTableDate], date: _date, direction_right = True) -> timedelta | None:
    'Counts the number of days without lessons'
    if not direction_right:
        schedule = reversed(schedule)

    res = None
    for day in schedule:
        day_date = datetime.strptime(day.date, '%Y-%m-%d').date()
        if direction_right:
            if day_date > date:
                res = day_date - date
                break
        else:
            if day_date < date:
                res = date - day_date
                break

    return res

def get_localized_date(context: ContextTypes.DEFAULT_TYPE, date: _date) -> str:
    date_localized = escape_markdown(format_date(date, locale=context._chat_data.get('lang_code')), version=2)
    week_day_localized = context._chat_data.get_lang()['text.time.week_day.' + str(date.weekday())]
    full_date_localized = f"*{date_localized}* `[`*{week_day_localized}*`]`"
    return full_date_localized

def create_schedule_section(context: ContextTypes.DEFAULT_TYPE, day: TimeTableDate) -> str:
    schedule_section = ''
    for lesson in day.lessons:
        for period in lesson.periods:
            # Escape ONLY USED api result not to break telegram markdown
            # DO NOT DELETE COMMENTS
            period.typeStr = escape_markdown(period.typeStr, version=2)
            period.classroom = escape_markdown(period.classroom, version=2)
#           period.disciplineFullName = escape_markdown(period.disciplineFullName, version=2)
            period.disciplineShortName = escape_markdown(period.disciplineShortName, version=2)
            period.timeStart = escape_markdown(period.timeStart, version=2)
            period.timeEnd = escape_markdown(period.timeEnd, version=2)
#           period.teachersName = escape_markdown(period.teachersName, version=2)
            period.teachersNameFull = escape_markdown(period.teachersNameFull, version=2)
#           period.chairName = escape_markdown(period.chairName, version=2)
#           period.dateUpdated = escape_markdown(period.dateUpdated, version=2)
#           period.groups = escape_markdown(period.groups, version=2)


            # If there are multiple teachers, display the first one and add +n to the end
            if ',' in period.teachersName:
                count = str(period.teachersNameFull.count(','))
                period.teachersName = period.teachersName[:period.teachersName.index(',')] + ' +' + count
                period.teachersNameFull = period.teachersNameFull[:period.teachersNameFull.index(',')] + ' +' + count

            schedule_section += context._chat_data.get_lang()['text.schedule.period'].format(
                **period.__dict__,
                lessonNumber=lesson.number
            )

    schedule_section += '`—――—―``―——``―—―``――``—``―``—``――――``――``―――`'
    return schedule_section



def create_message(context: ContextTypes.DEFAULT_TYPE, date: _date | str) -> dict:
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
        schedule = api.timetable_group(context._chat_data.get('group_id'), dateStart, dateEnd)
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 422:
            return invalid_group.create_message(context)
        return api_unavaliable.create_message(context)
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout
    ):
        return api_unavaliable.create_message(context)


    # Find schedule of current day
    cur_day_schedule = None
    for day in schedule:
        if day.date == date_str:
            cur_day_schedule = day
            break


    # Create the schedule page content
    lang = context._chat_data.get_lang()
    if cur_day_schedule is not None:
        msg_text = lang['page.schedule'].format(
            date=get_localized_date(context, date),
            schedule=create_schedule_section(context, cur_day_schedule)
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
            dateStart_localized = get_localized_date(context, date - skip_left + timedelta(days=1))
            dateEnd_localized = get_localized_date(context, date + skip_right - timedelta(days=1))
            msg_text = lang['page.schedule.empty.multiple_days'].format(
                dateStart=dateStart_localized,
                dateEnd=dateEnd_localized
            )
        # If no lessons for only one day
        else:
            msg_text = lang['page.schedule.empty'].format(date=get_localized_date(context, date))


    if cur_day_schedule is not None:
        next_day_date = date + timedelta(days=1)
        prev_day_date = date - timedelta(days=1)
        enable_today_button = date != _date.today()
    else:
        next_day_date = date + skip_right
        prev_day_date = date - skip_left
        enable_today_button = not next_day_date > _date.today() > prev_day_date

    # Create buttons
    buttons = [
        InlineKeyboardButton(text=lang['button.navigation.day_previous'], callback_data='open.schedule.day#date=' + prev_day_date.strftime('%Y-%m-%d')),
        InlineKeyboardButton(text=lang['button.navigation.day_next'], callback_data='open.schedule.day#date=' + next_day_date.strftime('%Y-%m-%d')),
        InlineKeyboardButton(text=lang['button.navigation.week_previous'], callback_data='open.schedule.day#date=' + (date - timedelta(days=7)).strftime('%Y-%m-%d')),
        InlineKeyboardButton(text=lang['button.navigation.week_next'], callback_data='open.schedule.day#date=' + (date + timedelta(days=7)).strftime('%Y-%m-%d')),
        InlineKeyboardButton(text=lang['button.menu'], callback_data='open.menu')
    ]
    # If the selected day is not today, then add "today" button
    if enable_today_button:
        buttons.append(InlineKeyboardButton(text=lang['button.navigation.today'], callback_data='open.schedule.today'))

    return {
        'text': msg_text,
        'reply_markup': InlineKeyboardMarkup(array_split(buttons, 2)),
        'parse_mode': 'MarkdownV2'
    }
