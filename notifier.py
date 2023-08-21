"""
Система сповіщень про наближення початку пар.

Перед кожним уроком надсилає повідомлення студентам
про те, що в них скоро пари. Звичайно, якщо вони є.

Працює на бібліотеці apscheduler із таймером cron.
Для кожного дзвінка створюється по 2 завдання, які
виконуються за 15 і за 1 хвилину до пари відповідно.

Кожне завдання ітерує всіх користувачів бота. Якщо у
користувача скоро пара, то йому надсилається повідомлення.
"""

import logging
from datetime import date, datetime, timedelta
from functools import partial

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings import bot, api
from bot.data import ChatDataManager
from bot.pages import classes_notification
from bot.errorhandler import send_error_to_telegram
from lib.api.exceptions import HTTPApiException

_logger = logging.getLogger(__name__)
API_RETRIES_LIMIT = 5


async def send_notification(chat_data: ChatDataManager, time_m: int):
    """Send notification to user if they have classes in X minutes."""

    schedule = api.timetable_group(chat_data.get('group_id'), date.today())

    msg = await bot.bot.send_message(
        chat_id=chat_data.chat_id,
        **classes_notification(chat_data, day=schedule[0], remaining=str(time_m)))

    chat_data.save_message(f'cl_notif_{time_m}m', msg)


async def send_notifications(lesson_number: int, time_m: int):
    """Send notifications to all users that have classes in X minutes."""

    api_retries = 0
    for chat_data in ChatDataManager.get_all():
        # Check if notification should be sent
        if not chat_data.get(f'cl_notif_{time_m}m') or \
                not chat_data.get('_accessible') or \
                chat_data.get('group_id') is None:
            continue

        try:
            if not is_lesson_in_interval(chat_data.get('group_id'), timedelta(minutes=time_m + 1)):
                continue
            await send_notification(chat_data, time_m)

        except HTTPApiException:
            _logger.error('API request failed. %s/%s', api_retries, API_RETRIES_LIMIT)

            api_retries += 1
            if api_retries >= API_RETRIES_LIMIT:
                break
            continue

        except Exception as e:
            _logger.exception('Unexpected error occurred while sending notifications.')
            await send_error_to_telegram(e)

    for call in calls:
        if call['number'] == lesson_number:
            call_time = datetime.strptime(call['timeStart'], '%H:%M')

            next_call_time = datetime.combine(
                datetime.today() + timedelta(days=1),
                (call_time - timedelta(minutes=time_m)).time())

            scheduler.add_job(
                partial(send_notifications, lesson_number=lesson_number, remaining_time=time_m),
                'date',
                next_run_time=next_call_time,
                id=f'cl_notif_{time_m}m_{lesson_number}',
                replace_existing=True)

            break


def is_lesson_in_interval(group_id: int, interval: timedelta) -> bool:
    """Check if there is a lesson in the given interval."""

    cur_dt = datetime.now()
    cur_time = cur_dt.time()
    with_interval = (cur_dt + interval).time()
    schedule = api.timetable_group(group_id, cur_dt.date())

    if len(schedule[0]['lessons']) == 0:
        return False

    first_lesson_number = schedule[0]['lessons'][0]['number']

    for call in calls:
        if call['number'] == first_lesson_number:
            call_time = datetime.strptime(call['timeStart'], '%H:%M').time()
            if cur_time <= call_time <= with_interval:
                return True

    return False


# Register jobs
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
        partial(send_notifications, lesson_number=_call['number'], time_m=15),
        'date',
        next_run_time=_call_time_15m,
        id=f'cl_notif_15m_{_call["number"]}',
        replace_existing=True
    )
    scheduler.add_job(
        partial(send_notifications, lesson_number=_call['number'], time_m=1),
        'date',
        next_run_time=_call_time_1m,
        id=f'cl_notif_1m_{_call["number"]}',
        replace_existing=True
    )


if __name__ == '__main__':
    # TODO
    pass
