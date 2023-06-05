"""
Notification system for classes.
Sends notifications to users that they have classes about to start.
"""

import logging
from datetime import date, datetime, timedelta
from functools import partial

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.data import ChatData
from bot.pages import classes_notification
from settings import bot, api
from lib.api.exceptions import HTTPApiException

_logger = logging.getLogger(__name__)
API_RETRIES_LIMIT = 5


def _get_day(chat_data: ChatData):
    try:
        day = api.timetable_group(chat_data.get('group_id'), date.today())[0]
    except HTTPApiException:
        return None
    return day


async def send_notification_15m(chat_data: ChatData):
    """Send notification to user that they have classes in 15 minutes."""

    day = _get_day(chat_data)
    if day is not None:
        msg = await bot.bot.send_message(chat_id=chat_data.chat_id,
                                         **classes_notification(chat_data, day, '15'))
        chat_data.save_message('cl_notif_15m', msg)


async def send_notification_1m(chat_data: ChatData):
    """Send notification to user that they have classes in 1 minute."""

    day = _get_day(chat_data)
    if day is not None:
        msg = await bot.bot.send_message(chat_id=chat_data.chat_id,
                                         **classes_notification(chat_data, day, '1'))
        chat_data.save_message('cl_notif_1m', msg)


async def send_notifications_15m(lesson_number: int):
    """Send notifications to all users that have classes in 15 minutes."""

    api_retries = 0
    for chat_data in ChatData.get_all():
        # Check if notification should be sent
        if not chat_data.get('cl_notif_15m') or \
                not chat_data.get('_accessible') or \
                chat_data.get('group_id') is None:
            continue

        try:
            if not is_lesson_in_interval(chat_data.get('group_id'), timedelta(minutes=20)):
                continue
        except HTTPApiException:
            _logger.error('API request failed. %s/%s', api_retries, API_RETRIES_LIMIT)

            api_retries += 1
            if api_retries >= API_RETRIES_LIMIT:
                break
            continue

        await send_notification_15m(chat_data)

    for call in calls:
        if call['number'] == lesson_number:
            call_time = datetime.strptime(call['timeStart'], '%H:%M')
            next_call_time = datetime.combine(datetime.today() + timedelta(days=1),
                                              (call_time - timedelta(minutes=15)).time())
            scheduler.add_job(
                partial(send_notifications_15m, lesson_number=lesson_number),
                'date',
                next_run_time=next_call_time,
                id=f'cl_notif_15m_{lesson_number}',
                replace_existing=True)
            break


async def send_notifications_1m(lesson_number: int):
    """Send notifications to all users that have classes in 1 minute."""

    api_retries = 0
    for chat_data in ChatData.get_all():
        if not chat_data.get('cl_notif_1m') or \
                not chat_data.get('_accessible') or \
                chat_data.get('group_id') is None:
            continue

        try:
            if not is_lesson_in_interval(chat_data.get('group_id'), timedelta(minutes=5)):
                continue

        except HTTPApiException:
            _logger.error('API request failed. %s/%s', api_retries, API_RETRIES_LIMIT)

            api_retries += 1
            if api_retries >= API_RETRIES_LIMIT:
                break
            continue

        await send_notification_1m(chat_data)

    for call in calls:
        if call['number'] == lesson_number:
            call_time = datetime.strptime(call['timeStart'], '%H:%M')
            next_call_time = datetime.combine(date.today() + timedelta(days=1),
                                              (call_time - timedelta(minutes=1)).time())
            scheduler.add_job(
                partial(send_notifications_1m, lesson_number=lesson_number),
                'date',
                next_run_time=next_call_time,
                id=f'cl_notif_1m_{lesson_number}',
                replace_existing=True)
            break


def is_lesson_in_interval(group_id: int, interval: timedelta) -> bool:
    """Check if there is a lesson in the given interval."""

    cur_dt = datetime.now()
    cur_time = cur_dt.time()
    with_interval = (cur_dt + interval).time()
    schedule = api.timetable_group(group_id, cur_dt.date())

    if len(schedule) == 0:
        return False

    first_lesson_number = schedule[0]['lessons'][0]['number']

    for call in calls:
        if call['number'] == first_lesson_number:
            call_time = datetime.strptime(call['timeStart'], '%H:%M').time()
            if cur_time < call_time < with_interval:
                return True

    return False


scheduler = AsyncIOScheduler(timezone='Europe/Kyiv')
calls = api.timetable_call_schedule()
_cur_time = datetime.now()
_today = datetime.today()

for _call in calls:
    _call_time = datetime.strptime(_call['timeStart'], '%H:%M')
    _call_time_15m = datetime.combine(_today, (_call_time - timedelta(minutes=15)).time())
    _call_time_1m = datetime.combine(_today, (_call_time - timedelta(minutes=1)).time())

    if _call_time_15m < _cur_time:
        _call_time_15m += timedelta(days=1)
    if _call_time_1m < _cur_time:
        _call_time_1m += timedelta(days=1)

    scheduler.add_job(
        partial(send_notifications_15m, lesson_number=_call['number']),
        'date',
        next_run_time=_call_time_15m,
        id=f'cl_notif_15m_{_call["number"]}',
        replace_existing=True
    )
    scheduler.add_job(
        partial(send_notifications_1m, lesson_number=_call['number']),
        'date',
        next_run_time=_call_time_1m,
        id=f'cl_notif_1m_{_call["number"]}',
        replace_existing=True
    )