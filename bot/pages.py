# pylint: disable=redefined-outer-name

"""
This module contains all bot pages.
"""

import os
from datetime import date as _date, timedelta

from babel.dates import format_date
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.helpers import escape_markdown
from requests.exceptions import RequestException, HTTPError

from lib.api.exceptions import HTTPApiException
from bot.data import ContextManager, ChatData
from bot.utils import array_split, clean_html, timeformatter, lessontime
from bot.teacherfinder import find_teacher_safe
from settings import api, langs, tg_logger, API_TYPE, API_TYPE_CACHED, TELEGRAM_SUPPORTED_HTML_TAGS


def access_denied(ctx: ContextManager) -> dict:
    """Access denied page"""

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu')
    ]]

    return {
        'text': ctx.lang.get('alert.no_permissions'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def admin_panel(ctx: ContextManager) -> dict:
    """Admin panel page"""

    buttons = [
        [InlineKeyboardButton(text=ctx.lang.get('button.admin.clear_expired_cache'),
                              callback_data='admin.clear_expired_cache')],
        [InlineKeyboardButton(text=ctx.lang.get('button.admin.get_logs'),
                              callback_data='admin.get_logs')],
        [InlineKeyboardButton(text=ctx.lang.get('button.admin.clear_logs'),
                              callback_data='admin.clear_logs')],
        [InlineKeyboardButton(text=ctx.lang.get('button.back'),
                              callback_data='open.menu')]
    ]

    return {
        'text': ctx.lang.get('page.admin_panel'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def api_unavaliable(ctx: ContextManager) -> dict:
    """API unavaliable page"""

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu'),
        InlineKeyboardButton(text=ctx.lang.get('button.write_me'),
                             url='https://t.me/cubicbyte')
    ]]

    return {
        'text': ctx.lang.get('page.api_unavaliable'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def calls(ctx: ContextManager) -> dict:
    """Calls page"""

    try:
        schedule_section = _get_calls_section_text()
    except HTTPApiException:
        return api_unavaliable(ctx)

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.back'),
                             callback_data='open.more'),
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu')
    ]]

    return {
        'text': ctx.lang.get('page.calls').format(schedule=schedule_section),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def classes_notification(chat_data: ChatData, day: dict, remaining: str) -> dict:
    """Classes notification page"""

    buttons = [[
        InlineKeyboardButton(text=chat_data.lang.get('button.open_schedule'),
                             callback_data=f'open.schedule.day#date={day["date"]}'),
        InlineKeyboardButton(text=chat_data.lang.get('button.settings'),
                             callback_data='open.settings')
    ]]

    return {
        'text': chat_data.lang.get('page.classes_notification').format(
            remaining=remaining,
            schedule=_get_notification_schedule_section(day)),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def course_list(ctx: ContextManager, structure_id: int, faculty_id: int) -> dict:
    """Course list page"""

    try:
        courses = api.list_courses(faculty_id, language=ctx.chat_data.get('lang_code'))
    except HTTPApiException:
        return api_unavaliable(ctx)

    buttons = [[
        InlineKeyboardButton(
            text=ctx.lang.get('button.back'),
            callback_data=f'select.schedule.structure#structureId={structure_id}')
    ]]

    for course in courses:
        buttons.append([
            InlineKeyboardButton(
                text=str(course['course']),
                callback_data=f'select.schedule.course#'
                    + f'structureId={structure_id}&'
                    + f'facultyId={faculty_id}&'
                    + f'course={course["course"]}')
        ])

    return {
        'text': ctx.lang.get('page.course'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def faculty_list(ctx: ContextManager, structure_id: int) -> dict:
    """Faculty list page"""

    try:
        faculties = api.list_faculties(structure_id, language=ctx.chat_data.get('lang_code'))
        structures = api.list_structures(language=ctx.chat_data.get('lang_code'))
    except HTTPApiException:
        return api_unavaliable(ctx)

    buttons = []

    if len(structures) > 1:
        buttons.append([
            InlineKeyboardButton(
                text=ctx.lang.get('button.back'),
                callback_data='open.select_group')
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text=ctx.lang.get('button.back'),
                callback_data='open.menu')
        ])

    for faculty in faculties:
        buttons.append([
            InlineKeyboardButton(
                text=faculty['fullName'],
                callback_data=f'select.schedule.faculty#'
                    + f'structureId={structure_id}&'
                    + f'facultyId={faculty["id"]}')
        ])

    return {
        'text': ctx.lang.get('page.faculty'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def greeting(ctx: ContextManager) -> dict:
    """Greeting page"""

    return {
        'text': ctx.lang.get('page.greeting'),
        'parse_mode': 'MarkdownV2'
    }


def group_list(ctx: ContextManager, structure_id: int, faculty_id: int, course: int) -> dict:
    """Group list page"""

    try:
        groups = api.list_groups(faculty_id, course, language=ctx.chat_data.get('lang_code'))
    except HTTPApiException:
        return api_unavaliable(ctx)

    buttons = [[
        InlineKeyboardButton(
            text=ctx.lang.get('button.back'),
            callback_data=f'select.schedule.faculty#'
                + f'structureId={structure_id}&'
                + f'facultyId={faculty_id}')
    ]]

    group_btns = []
    for group in groups:
        group_btns.append(
            InlineKeyboardButton(
                text=group['name'],
                callback_data=f'select.schedule.group#groupId={group["id"]}')
        )

    # Make many 3-wide button rows like this: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    buttons.extend(array_split(group_btns, 3))

    return {
        'text': ctx.lang.get('page.group'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def info(ctx: ContextManager) -> dict:
    """Info page"""

    try:
        api_ver = escape_markdown(api.version()['name'], version=2)
    except RequestException:
        api_ver = ctx.lang.get('text.unknown')

    message_text = ctx.lang.get('page.info').format(
        api_ver=api_ver,
        api_ver_supported=escape_markdown(api.VERSION, version=2)
    )

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.back'),
                             callback_data='open.more'),
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu')
    ]]

    return {
        'text': message_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def invalid_group(ctx: ContextManager) -> dict:
    """Invalid group page"""

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.select_group'),
                             callback_data='open.select_group'),
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu')
    ]]

    return {
        'text': ctx.lang.get('page.invalid_group'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def lang_selection(ctx: ContextManager) -> dict:
    """Language selection page"""

    buttons = []

    for lang_name, lang in langs.items():
        buttons.append([
            InlineKeyboardButton(text=lang.get('lang_name'),
                                 callback_data=f'select.lang#lang={lang_name}')
        ])

    buttons.append([
        InlineKeyboardButton(text=ctx.lang.get('button.back'),
                             callback_data='open.settings'),
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu')
    ])

    return {
        'text': ctx.lang.get('page.lang_select').format(
            lang=ctx.lang.get('lang_name')),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def left(ctx: ContextManager) -> dict:
    """Left page"""

    if ctx.chat_data.get('group_id') is None:
        return invalid_group(ctx)

    try:
        schedule = api.timetable_group(ctx.chat_data.get('group_id'), _date.today())
        if len(schedule) != 0:
            rem_time = lessontime.get_calls_status(schedule[0]['lessons'])
    except HTTPApiException:
        return api_unavaliable(ctx)

    # If there is no classes
    if len(schedule) == 0 or rem_time is None or rem_time['status'] == 'ended':
        return {
            'text': ctx.lang.get('page.left.no_more'),
            'reply_markup': InlineKeyboardMarkup([[
                InlineKeyboardButton(text=ctx.lang.get('button.back'), callback_data='open.more'),
                InlineKeyboardButton(text=ctx.lang.get('button.menu'), callback_data='open.menu'),
            ]]),
            'parse_mode': 'MarkdownV2'
        }

    time_formatted = timeformatter.format_time(
        lang_code=ctx.chat_data.get('lang_code'),
        time=rem_time['time'], depth=2)

    # Lesson is going
    if rem_time['status'] == 'going':
        page_text = ctx.lang.get('page.left.to_end').format(
            left=escape_markdown(time_formatted, version=2))

    # Classes is not started yet or it's break
    else:
        page_text = ctx.lang.get('page.left.to_start').format(
            left=escape_markdown(time_formatted, version=2))

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.menu'), callback_data='open.menu'),
        InlineKeyboardButton(text=ctx.lang.get('button.refresh'), callback_data='open.left')
    ]]

    return {
        'text': page_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def menu(ctx: ContextManager) -> dict:
    """Menu page"""

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.schedule'),
                             callback_data='open.schedule.today')
    ], [
        InlineKeyboardButton(text=ctx.lang.get('button.settings'),
                             callback_data='open.settings'),
        InlineKeyboardButton(text=ctx.lang.get('button.more'),
                             callback_data='open.more')
    ]]

    # If user is admin, then add "control panel" button
    if ctx.user_data.get('admin'):
        buttons.append([
            InlineKeyboardButton(text=ctx.lang.get('button.admin.panel'),
                                 callback_data='admin.open_panel')
        ])

    return {
        'text': ctx.lang.get('page.menu'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def more(ctx: ContextManager) -> dict:
    """More page"""

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.calls'),
                             callback_data='open.calls'),
        InlineKeyboardButton(text=ctx.lang.get('button.left'),
                             callback_data='open.left')
    ], [
        InlineKeyboardButton(text=ctx.lang.get('button.info'),
                             callback_data='open.info')
    ], [
        InlineKeyboardButton(text=ctx.lang.get('button.back'),
                             callback_data='open.menu')
    ]]

    return {
        'text': ctx.lang.get('page.more'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def schedule(ctx: ContextManager, date: _date | str) -> dict:
    """Schedule page"""

    # Create "date_str" and "date" variables
    if isinstance(date, _date):
        date_str = date.isoformat()
    else:
        date_str = date
        date = _date.fromisoformat(date_str)

    # Get schedule
    date_start = date - timedelta(days=date.weekday() + 7)
    date_end = date_start + timedelta(days=20)
    try:
        schedule = api.timetable_group(ctx.chat_data.get('group_id'), date_start, date_end,
                                    language=ctx.chat_data.get('lang_code'))

    except HTTPError as err:
        if err.response.status_code == 422:
            return invalid_group(ctx)
        return api_unavaliable(ctx)

    except HTTPApiException:
        return api_unavaliable(ctx)


    # Find schedule of current day
    cur_day_schedule = None
    for day in schedule:
        if day['date'] == date_str:
            cur_day_schedule = day
            break

    if cur_day_schedule is not None:
        # Schedule page
        return day_schedule(ctx, date, cur_day_schedule)

    # "no lessons" page
    return empty_schedule(ctx, schedule, date, date_start, date_end)


def day_schedule(ctx: ContextManager, date: _date, day: dict) -> dict:
    """Schedule page"""

    lang = ctx.lang

    msg_text = ctx.lang.get('page.schedule').format(
        date=_get_localized_date(ctx, date),
        schedule=_create_schedule_section(ctx, day)
    )

    # Create buttons
    buttons = [
        InlineKeyboardButton(text=lang.get('button.navigation.day_previous'),
                             callback_data='open.schedule.day#date='
                             + (date - timedelta(days=1)).isoformat()),
        InlineKeyboardButton(text=lang.get('button.navigation.day_next'),
                             callback_data='open.schedule.day#date='
                             + (date + timedelta(days=1)).isoformat()),
        InlineKeyboardButton(text=lang.get('button.navigation.week_previous'),
                             callback_data='open.schedule.day#date='
                             + (date - timedelta(days=7)).isoformat()),
        InlineKeyboardButton(text=lang.get('button.navigation.week_next'),
                             callback_data='open.schedule.day#date='
                             + (date + timedelta(days=7)).isoformat()),
        InlineKeyboardButton(text=lang.get('button.menu'), callback_data='open.menu')
    ]

    # "Today" button
    if date != _date.today():
        buttons.append(InlineKeyboardButton(
            text=lang.get('button.navigation.today'),
            callback_data='open.schedule.today'
        ))

    # Split buttons into 2-wide rows
    buttons = array_split(buttons, 2)

    # "Additional info" button
    if _check_extra_text(day):
        buttons.append([InlineKeyboardButton(
            text=lang.get('button.schedule.extra'),
            callback_data='open.schedule.extra#date=' + date.isoformat()
        )])


    return {
        'text': msg_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2',
        'disable_web_page_preview': True
    }


def empty_schedule(ctx: ContextManager, schedule: list[dict],
                   date: _date, from_date: _date, to_date: _date) -> dict:
    """Empty schedule page"""

    # TODO remove from_date and to_date. Now, if we call timetable_group(today, today+5),
    # we will get an array with size 0-6, but it should be fixed 6.

    lang = ctx.lang

    # Number of days you need to skip to reach a day with lessons
    skip_left = _count_no_lesson_days(schedule, date, direction_right=False)
    skip_right = _count_no_lesson_days(schedule, date, direction_right=True)
    if skip_right is None:
        skip_right = (to_date - date).days
    if skip_left is None:
        skip_left = (date - from_date).days

    # Decide whether to show the "today" button, and also
    # decide the "next" and "previous" buttons skip values
    next_day_date = date + timedelta(days=skip_right)
    prev_day_date = date - timedelta(days=skip_left)
    next_week_date = from_date + timedelta(days=7)
    prev_week_date = from_date - timedelta(days=7)
    enable_today_button = not next_day_date > _date.today() > prev_day_date

    # If there are no lessons for multiple days
    # Then combine all the days without lessons into one page
    if skip_left > 1 or skip_right > 1:
        msg_text = lang.get('page.schedule.empty.multiple_days').format(
            dateStart=_get_localized_date(ctx, prev_day_date + timedelta(days=1)),
            dateEnd=  _get_localized_date(ctx, next_day_date - timedelta(days=1)),
        )

        next_week_date = max(next_week_date, next_day_date)
        prev_week_date = min(prev_week_date, prev_day_date)
    else:
        # If no lessons for only one day
        msg_text = lang.get('page.schedule.empty').format(date=_get_localized_date(ctx, date))


    # Create buttons
    buttons = [
        InlineKeyboardButton(text=lang.get('button.navigation.day_previous'),
                             callback_data='open.schedule.day#date='
                             + prev_day_date.isoformat()),
        InlineKeyboardButton(text=lang.get('button.navigation.day_next'),
                             callback_data='open.schedule.day#date='
                             + next_day_date.isoformat()),
        InlineKeyboardButton(text=lang.get('button.navigation.week_previous'),
                             callback_data='open.schedule.day#date='
                             + prev_week_date.isoformat()),
        InlineKeyboardButton(text=lang.get('button.navigation.week_next'),
                             callback_data='open.schedule.day#date='
                             + next_week_date.isoformat()),
        InlineKeyboardButton(text=lang.get('button.menu'), callback_data='open.menu')
    ]

    if enable_today_button:
        buttons.append(InlineKeyboardButton(
            text=lang.get('button.navigation.today'),
            callback_data='open.schedule.today'
        ))

    # Split buttons into 2-wide rows
    buttons = array_split(buttons, 2)


    return {
        'text': msg_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def schedule_extra(ctx: ContextManager, date: _date | str) -> dict:
    """Schedule extra information page"""

    if isinstance(date, _date):
        date_str = date.isoformat()
    else:
        date_str = date
        date = _date.fromisoformat(date)

    # Get schedule
    try:
        schedule = api.timetable_group(ctx.chat_data.get('group_id'), date_str,
                                       language=ctx.chat_data.get('lang_code'))
    except HTTPApiException:
        return api_unavaliable(ctx)

    # Find schedule of current day
    cur_day_schedule = None
    for day in schedule:
        if day['date'] == date_str:
            cur_day_schedule = day
            break

    if cur_day_schedule is None:
        return empty_schedule(ctx, schedule, date, date, date)

    page_text = ''

    for lesson in cur_day_schedule['lessons']:
        for period in lesson['periods']:
            if period['extraText']:
                extra_text = api.timetable_ad(
                    period['r1'], date_str,
                    language=ctx.chat_data.get('lang_code'))['html']
                extra_text = clean_html(extra_text, tags_whitelist=TELEGRAM_SUPPORTED_HTML_TAGS)
                extra_text = extra_text.strip()
                page_text += f'\n\n<pre>{lesson["number"]})</pre> {extra_text}'

    return {
        'text': ctx.lang.get('page.schedule.extra').format(page_text[2:]),
        'reply_markup': InlineKeyboardMarkup([[
            InlineKeyboardButton(text=ctx.lang.get('button.back'),
                                 callback_data='open.schedule.day#date=' + date_str)
        ]]),
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }


def settings(ctx: ContextManager) -> dict:
    """Settings menu page"""

    lang = ctx.lang
    cl_notif_15m_enabled = ctx.chat_data.get('cl_notif_15m')
    cl_notif_1m_enabled = ctx.chat_data.get('cl_notif_1m')

    # Get chat group name
    if ctx.chat_data.get('group_id') is not None:
        if API_TYPE == API_TYPE_CACHED:
            group = escape_markdown(api.cache.get_group(
                ctx.chat_data.get('group_id'))[2], version=2)
        else:
            group = ctx.chat_data.get('group_id')
    else:
        group = lang.get('text.not_selected')

    buttons = [[
        InlineKeyboardButton(
            text=lang.get('button.select_group'),
            callback_data='open.select_group'),
        InlineKeyboardButton(
            text=lang.get('button.select_lang'),
            callback_data='open.select_lang')
    ], [
        InlineKeyboardButton(
            text=lang.get('button.settings.cl_notif_15m'),
            callback_data=f'set.cl_notif_15m#state={int(not cl_notif_15m_enabled)}')
    ], [
        InlineKeyboardButton(
            text=lang.get('button.settings.cl_notif_1m'),
            callback_data=f'set.cl_notif_1m#state={int(not cl_notif_1m_enabled)}')
    ], [
        InlineKeyboardButton(
            text=lang.get('button.back'),
            callback_data='open.menu')
    ]]

    def get_icon(setting: bool) -> str:
        return '✅' if setting else '❌'

    page_text = lang.get('page.settings').format(
        group_id=group,
        cl_notif_15m=get_icon(cl_notif_15m_enabled),
        cl_notif_1m=get_icon(cl_notif_1m_enabled)
    )

    return {
        'text': page_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def statistic(ctx: ContextManager) -> dict:
    """Statistic page"""

    chat_dir = tg_logger.get_chat_log_dir(ctx.update.effective_chat.id)

    # Get first message date and message count
    with open(os.path.join(chat_dir, 'messages.txt'), encoding='utf-8') as file:
        messages = 0
        for messages, line in enumerate(file):
            if messages == 0:
                first_msg_date = line[1:line.index(']')]

    # Get number of button clicks
    with open(os.path.join(chat_dir, 'cb_queries.txt'), encoding='utf-8') as file:
        clicks = 0
        for clicks, _ in enumerate(file):
            pass

    message_text = '*Statistic*\n\n'
    message_text += f'This chat ID: {ctx.update.effective_chat.id}\n'
    message_text += f'Your ID: {ctx.update.effective_user.id}\n'
    message_text += f'Messages: {messages}\n'
    message_text += f'Button clicks: {clicks}\n'
    message_text += f'First message: {escape_markdown(first_msg_date, version=2)}'

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.menu'),
                             callback_data='open.menu'),
        InlineKeyboardButton(text='How Did We Get Here?',
                             url='https://github.com/cubicbyte/dteubot')
    ]]

    return {
        'text': message_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def structure_list(ctx: ContextManager) -> dict:
    """Structures list menu page"""

    try:
        structures = api.list_structures(language=ctx.chat_data.get('lang_code'))
    except HTTPApiException:
        return api_unavaliable(ctx)

    # If there is only one structure, show faculties page
    if len(structures) == 1:
        return faculty_list(ctx, structures[0]['id'])

    buttons = [[
        InlineKeyboardButton(text=ctx.lang.get('button.back'), callback_data='open.menu')
    ]]

    for structure in structures:
        buttons.append([
            InlineKeyboardButton(
                text=structure['fullName'],
                callback_data=f'select.schedule.structure#structureId={structure["id"]}')
        ])

    return {
        'text': ctx.lang.get('page.structure'),
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }


def error(ctx: ContextManager) -> dict:
    """Error page"""

    return {
        'text': ctx.lang.get('page.error'),
        'reply_markup': InlineKeyboardMarkup([[
            InlineKeyboardButton(text=ctx.lang.get('button.menu'), callback_data='open.menu')
        ]]),
        'parse_mode': 'MarkdownV2'
    }









def _get_calls_section_text() -> str:
    """
    Get calls section text in the calls page

    ## Example:
    ```
    1) 08:20 - 09:40
    2) 10:05 - 11:25
    3) 12:05 - 13:25
    4) 13:50 - 15:10
    5) 15:25 - 16:45
    6) 17:00 - 18:20
    7) 18:30 - 19:50
    8) 19:55 - 21:40
    ```
    """

    parts = []

    for call in api.timetable_call_schedule():
        number = call['number']
        time_start = call['timeStart']
        time_end = call['timeEnd']

        parts.append(f'`{number})` *{time_start}* `-` *{time_end}*')

    return '\n'.join(parts)


def _get_notification_schedule_section(day: dict) -> str:
    """
    Creates a schedule section for the notification page

    ## Example:
    ```
    2) ІнМов за ПроСпр[КонсЕкз]
    3) "В" МатемЛогіка[КонсЕкз]
    ```
    """
    str_format = '`{0})` *{1}*`[{2}]`\n'
    section = ''

    for lesson in day['lessons']:
        for period in lesson['periods']:
            section += str_format.format(
                lesson['number'],
                escape_markdown(period['disciplineShortName'], version=2),
                escape_markdown(period['typeStr'], version=2))

    return section[:-1]


def _count_no_lesson_days(
        schedule: list[dict],
        date: _date,
        direction_right=True) -> int | None:
    """
    Counts the number of days without lessons
    """

    if not direction_right:
        schedule = reversed(schedule)

    for day in schedule:
        day_date = _date.fromisoformat(day['date'])
        if direction_right:
            if day_date > date:
                days_timedelta = day_date - date
                break
        else:
            if day_date < date:
                days_timedelta = date - day_date
                break
    else:
        return None

    return days_timedelta.days


def _get_localized_date(ctx: ContextManager, date: _date) -> str:
    """
    Returns a localized date string

    Example:
    --------
    📅 18 трав. 2023 р. [П'ятниця] 📅
    """

    date_localized = escape_markdown(format_date(
        date, locale=ctx.chat_data.get('lang_code')), version=2)
    week_day_localized = ctx.lang.get('text.time.week_day.' + str(date.weekday()))
    full_date_localized = f"*{date_localized}* `[`*{week_day_localized}*`]`"

    return full_date_localized


def _create_schedule_section(ctx: ContextManager, day: dict) -> str:
    """
    Creates a schedule section for the schedule page

    ## Example:
    ```
    ———— 10:05 ——— 11:25 ————
      ІнМов за ПроСпр[КонсЕкз]
    2 Онлайн
      Кулаженко Олена Петрiвна +1
    ———— 12:05 ——— 13:25 ————
      "В" МатемЛогіка[КонсЕкз]
    3 Онлайн
      Котляр Валерій Юрійович
    —――—――——―—―――—―—―――――――――
    ```
    """

    schedule_section = ''

    for lesson in day['lessons']:
        for period in lesson['periods']:
            name = period['teachersNameFull']
            multiple_teachers = ', ' in name

            if multiple_teachers:
                name = name.split(', ')[0]

            name = escape_markdown(name, version=2)
            teacher = find_teacher_safe(name)

            # Escape ONLY USED api result not to break telegram markdown
            # DO NOT DELETE COMMENTS
            # period['disciplineFullName'] \
            #     = escape_markdown(period['disciplineFullName'], version=2)
            period['disciplineShortName'] \
                = escape_markdown(period['disciplineShortName'], version=2)
            period['typeStr'] = escape_markdown(period['typeStr'], version=2)
            period['classroom'] = escape_markdown(period['classroom'], version=2)
            period['timeStart'] = escape_markdown(period['timeStart'], version=2)
            period['timeEnd'] = escape_markdown(period['timeEnd'], version=2)
            # period['teachersName'] = escape_markdown(period['teachersName'], version=2)
            # period['teachersNameFull'] = escape_markdown(period['teachersNameFull'], version=2)
            # period['chairName'] = escape_markdown(period['chairName'], version=2)
            # period['dateUpdated'] = escape_markdown(period['dateUpdated'], version=2)
            # period['groups'] = escape_markdown(period['groups'], version=2)

            # If there are multiple teachers, display the first one and add +n to the end

            if teacher:
                name = f'[{name}]({teacher.page_link})'

            if multiple_teachers:
                count = str(period['teachersNameFull'].count(','))
                name += ' \\+' + count

            period['teachersNameFull'] = name

            schedule_section += ctx.lang.get('text.schedule.period').format(
                **period,
                lessonNumber=lesson['number']
            )

    schedule_section += '`—――—―``―——``―—―``――``—``―``—``――――``――``―――`'
    return schedule_section


def _check_extra_text(day: dict) -> bool:
    """Checks if the day schedule has extra text, like zoom links, etc."""

    for lesson in day['lessons']:
        for period in lesson['periods']:
            if period['extraText']:
                return True

    return False
