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

    next_call = get_next_call(calls) or calls[0]
    call_time = datetime.strptime(next_call.timeStart, '%H:%M')
    next_call_time = datetime.combine(datetime.today() + timedelta(days=1), (call_time - timedelta(seconds=offset_s)).time())
    scheduler.add_job(
        partial(send_notifications, offset_s=offset_s),
        'date',
        next_run_time=next_call_time,
        id='cl_notif_%ds' % offset_s,
        replace_existing=True
    )

def get_next_call(calls: List[CallSchedule]) -> CallSchedule | None:
    cur_time = datetime.now().time()
    for call in calls:
        call_time = datetime.strptime(call.timeStart, '%H:%M').time()
        if cur_time < call_time:
            return call
    return None

def is_lesson_in_interval(group_id: int, interval: timedelta) -> bool:
    cur_dt = datetime.now()
    cur_time = cur_dt.time()
    with_interval = (cur_dt + interval).time()
    schedule = api.timetable_group(group_id, cur_dt.date())
    if len(schedule) == 0:
        return False
    calls = api.timetable_call_schedule()
    first_lesson_number = schedule[0].lessons[0].number
    for call in calls:
        if call.number == first_lesson_number:
            call_time = datetime.strptime(call.timeStart, '%H:%M').time()
            if cur_time < call_time < with_interval:
                return True
    return False

def setup(scheduler: AsyncIOScheduler):
    _today = datetime.today()
    _next_call = get_next_call(calls)

    if _next_call is None:
        _next_call_time = datetime.combine(_today + timedelta(days=1), datetime.strptime(calls[0].timeStart, '%H:%M').time())
    else:
        _next_call_time = datetime.combine(_today, datetime.strptime(_next_call.timeStart, '%H:%M').time())

    # 15 minutes before
    scheduler.add_job(
        partial(send_notifications, offset_s=900),
        'date',
        next_run_time=_next_call_time - timedelta(minutes=15),
        id='cl_notif_900s',
        replace_existing=True
    )
    # 1 minute before
    scheduler.add_job(
        partial(send_notifications, offset_s=60),
        'date',
        next_run_time=_next_call_time - timedelta(minutes=1),
        id='cl_notif_60s',
        replace_existing=True
    )


scheduler = AsyncIOScheduler(timezone='Europe/Kyiv')
calls = api.timetable_call_schedule()
setup(scheduler)
