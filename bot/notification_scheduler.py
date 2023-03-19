from datetime import date, datetime, timedelta
from functools import partial
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .data import ChatData
from .pages import classes_notification
from .settings import bot, api

async def send_notification_15m(chat_data: ChatData):
    day = api.timetable_group(chat_data.group_id, date.today())[0]
    await bot.bot.send_message(chat_id=chat_data._chat_id, **classes_notification.create_message_15m(chat_data, day))

async def send_notification_1m(chat_data: ChatData):
    day = api.timetable_group(chat_data.group_id, date.today())[0]
    await bot.bot.send_message(chat_id=chat_data._chat_id, **classes_notification.create_message_1m(chat_data, day))

async def send_notifications_15m(lesson_number: int):
    for chat_data in ChatData.get_all():
        if not chat_data.cl_notif_15m or not chat_data._accessible or chat_data.group_id is None:
            continue

        if not is_lesson_in_interval(chat_data.group_id, timedelta(minutes=20)):
            continue

        await send_notification_15m(chat_data)

    for call in calls:
        if call.number == lesson_number:
            call_time = datetime.strptime(call.timeStart, '%H:%M')
            next_call_time = datetime.combine(datetime.today() + timedelta(days=1), (call_time - timedelta(minutes=15)).time())
            scheduler.add_job(
                partial(send_notifications_15m, lesson_number=lesson_number),
                'date',
                next_run_time=next_call_time,
                id='cl_notif_15m_%d' % lesson_number,
                replace_existing=True)
            break

async def send_notifications_1m(lesson_number: int):
    for chat_data in ChatData.get_all():
        if not chat_data.cl_notif_1m or not chat_data._accessible or chat_data.group_id is None:
            continue

        if not is_lesson_in_interval(chat_data.group_id, timedelta(minutes=5)):
            continue

        await send_notification_1m(chat_data)

    for call in calls:
        if call.number == lesson_number:
            call_time = datetime.strptime(call.timeStart, '%H:%M')
            next_call_time = datetime.combine(datetime.today() + timedelta(days=1), (call_time - timedelta(minutes=1, seconds=30)).time())
            scheduler.add_job(
                partial(send_notifications_1m, lesson_number=lesson_number),
                'date',
                next_run_time=next_call_time,
                id='cl_notif_1m_%d' % lesson_number,
                replace_existing=True)
            break

def is_lesson_in_interval(group_id: int, interval: timedelta) -> bool:
    cur_time = datetime.now()
    schedule = api.timetable_group(group_id, date.today())
    if len(schedule) == 0:
        return False
    calls = api.timetable_call_schedule()
    first_lesson_number = schedule[0].lessons[0].number
    for call in calls:
        if call.number == first_lesson_number:
            call_time = datetime.strptime(call.timeStart, '%H:%M')
            if cur_time < call_time < cur_time + interval:
                return True
    return False



scheduler = AsyncIOScheduler(timezone='Europe/Kyiv')
calls = api.timetable_call_schedule()
_cur_time = datetime.now()
_today = datetime.today()

for call in calls:
    _call_time = datetime.strptime(call.timeStart, '%H:%M')
    _call_time_15m = datetime.combine(_today, (_call_time - timedelta(minutes=15)).time())
    _call_time_1m = datetime.combine(_today, (_call_time - timedelta(minutes=1, seconds=30)).time())

    if _call_time_15m < _cur_time:
        _call_time_15m += timedelta(days=1)
    if _call_time_1m < _cur_time:
        _call_time_1m += timedelta(days=1)

    scheduler.add_job(
        partial(send_notifications_15m, lesson_number=call.number),
        'date',
        next_run_time=_call_time_15m,
        id='cl_notif_15m_%d' % call.number,
        replace_existing=True
    )
    scheduler.add_job(
        partial(send_notifications_1m, lesson_number=call.number),
        'date',
        next_run_time=_call_time_1m,
        id='cl_notif_1m_%d' % call.number,
        replace_existing=True
    )