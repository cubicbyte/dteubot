import logging
import requests.exceptions
from typing import List
from datetime import date, datetime, timedelta
from functools import partial
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from lib.api.schemas import CallSchedule
from .data import ChatData, Message
from .pages import classes_notification
from .settings import bot, api

_logger = logging.getLogger(__name__)
api_retries_limit = 5


def _get_day(chat_data: ChatData):
    try:
        day = api.timetable_group(chat_data.get('group_id'), date.today())[0]
    except (
        requests.exceptions.ConnectionError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.HTTPError
    ):
        return None
    return day

async def send_notification(chat_data: ChatData, remaining: str):
    if (day := _get_day(chat_data)) is not None:
        msg = await bot.bot.send_message(chat_id=chat_data._chat_id, **classes_notification.create_message(chat_data, day, remaining))
        chat_data.add_message(Message(msg.message_id, msg.date, 'cl_notif_%sm' % remaining, chat_data.get('lang_code')))

async def send_notifications(offset_s: int):
    api_retries = 0
    remaining = str(offset_s // 60)
    for chat_data in ChatData.get_all():
        if not chat_data.get(f'cl_notif_{remaining}m') or not chat_data.get('_accessible') or chat_data.get('group_id') is None:
            continue

        try:
            if not is_lesson_in_interval(chat_data.get('group_id'), timedelta(seconds=offset_s + 60)):
                continue
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
            requests.exceptions.HTTPError
        ):
            api_retries += 1
            _logger.error(f'API request failed. {api_retries}/{api_retries_limit}')
            if api_retries >= api_retries_limit:
                break
            continue

        await send_notification(chat_data, remaining)

def register_loop_iteration(offset_s: int):
    next_call = get_next_call(calls)
    if next_call is None:
        next_call_time = datetime.combine(datetime.today() + timedelta(days=1), (datetime.strptime(calls[0].timeStart, '%H:%M') - timedelta(seconds=offset_s)).time())
    else:
        next_call_time = datetime.combine(datetime.today(), (datetime.strptime(next_call.timeStart, '%H:%M') - timedelta(seconds=offset_s)).time())
    scheduler.add_job(
        partial(notification_loop, offset_s=offset_s),
        'date',
        next_run_time=next_call_time,
        id='cl_notif_%ds' % offset_s,
        replace_existing=True
    )

async def notification_loop(offset_s: int):
    _logger.info(f'Sending notifications (offset: {offset_s}s)')
    await send_notifications(offset_s)
    _logger.info(f'Registering next iteration (offset: {offset_s}s)')
    register_loop_iteration(offset_s)

def get_next_call(calls: List[CallSchedule]) -> CallSchedule | None:
    for call in calls:
        if datetime.now().time() < call.get_time_start():
            return call
    return None

def is_lesson_in_interval(group_id: int, interval: timedelta) -> bool:
    cur_dt = datetime.now()
    schedule = api.timetable_group(group_id, cur_dt.date())
    if len(schedule) == 0:
        return False
    calls = api.timetable_call_schedule()
    first_lesson_number = schedule[0].lessons[0].number
    for call in calls:
        if call.number == first_lesson_number:
            if cur_dt.time() < call.get_time_start() < (cur_dt + interval).time():
                return True
    return False

scheduler = AsyncIOScheduler(timezone='Europe/Kyiv', job_defaults={'apscheduler.job_defaults.max_instances': 2})
calls = api.timetable_call_schedule()
register_loop_iteration(offset_s=900) # 15 min
register_loop_iteration(offset_s=60)  # 1 min
