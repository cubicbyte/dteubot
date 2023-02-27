from dataclasses import dataclass
from datetime import datetime, timedelta
from .settings import api
from .utils.format_time import format_time

@dataclass
class FormattedTime:
    time: timedelta
    text: str

def get_lesson(calls: list, lessons: list[int], timestamp = datetime.now()) -> dict:
    """Returns the current time relative to today's lessons
    
    Example
    --------------
    >>> api.get_lesson([1, 2, 3, 4])
    {
        "lesson": {
            "number: 0,
            "timeStart": <datetime.datetime>,
            "timeEnd": <datetime.datetime>
        },
        "status": 0,
        "time": <datetime.timedelta>
    }
    Fields
    --------------
    - lesson: lesson
    - status:\n
        0 - before 1st lesson\n
        1 - during lesson\n
        2 - during the break\n
        3 - after last lesson
    - time: time to lesson
    """

    lessons.sort()

    cur_time = datetime.now()
    cur_date = cur_time.date()
    calls_formatted = {}
    for call in calls:
        timeStart = datetime.combine(cur_date, datetime.strptime(call['timeStart'], '%H:%M').time())
        timeEnd = datetime.combine(cur_date, datetime.strptime(call['timeEnd'], '%H:%M').time())
        calls_formatted[str(call['number'])] = {
            'number': call['number'],
            'timeStart': timeStart,
            'timeEnd': timeEnd
        }

    result = {
        'lesson': None,
        'status': None,
        'time': None
    }

    # if the first lesson has not started
    if cur_time < calls_formatted[str(lessons[0])]['timeStart']:
        result['lesson'] = calls[0]
        result['status'] = 0
        result['time'] = calls_formatted[str(lessons[0])]['timeStart'] - cur_time
    # If the last lesson is over
    elif cur_time > calls_formatted[str(lessons[-1])]['timeEnd']:
        result['lesson'] = calls[-1]
        result['status'] = 3
        result['time'] = cur_time - calls_formatted[str(lessons[-1])]['timeEnd']
    else:
        for i in lessons:
            lesson = calls_formatted[str(i)]
            if cur_time <= lesson['timeEnd']:
                cur_lesson = lesson
                break

        if cur_time < cur_lesson['timeStart']:
            result['lesson'] = cur_lesson
            result['status'] = 2
            result['time'] = cur_lesson['timeStart'] - cur_time
        else:
            result['lesson'] = cur_lesson
            result['status'] = 1
            result['time'] = cur_lesson['timeEnd'] - cur_time

    return result

def get_time(groupId: int, timestamp = datetime.now()) -> dict | None:
    """Returns the time before the start/end of the lesson"""

    date = timestamp.date()
    schedule = api.timetable_group(groupId, date, date)
    calls = api.timetable_call_schedule()
    date = timestamp.strftime('%Y-%m-%d')

    # If there are no lessons, return None
    day = None
    for i in schedule:
        if i['date'] == date:
            day = i
            break
    if day is None:
        return None

    lessons = []
    for lesson in day['lessons']:
        lessons.append(lesson['number'])

    return get_lesson(calls, lessons)

def get_time_formatted(lang_code: str, groupId: int, timestamp = datetime.now()) -> dict:
    remaining_time = get_time(groupId, timestamp)

    if remaining_time is None:
        formatted = None
    else:
        short = remaining_time['status'] == 1 or remaining_time['status'] == 2
        depth = 2 if short else 1
        formatted = format_time(lang_code, remaining_time['time'], depth=depth, short=short)

    result = {
        'time': remaining_time,
        'text': formatted
    }

    return result
