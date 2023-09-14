"""
Module for working with the time relative of the lessons
"""

from datetime import datetime
from settings import api


def get_calls_status(
        lessons: list[dict],
        calls: list[dict] | None = None,
        timestamp: datetime | None = None
) -> dict | None:
    """
    Returns the time relative to calls

    Example
    -------
    >>> get_calls_status()
    {
        "status": 'not_started',
        "call": <CallSchedule>,
        "time": <datetime.timedelta>,
        "time_start": <datetime.datetime>,
        "time_end": <datetime.datetime>
    }

    Fields
    ------
    - status:
        - 'not_started' - before 1st lesson
        - 'going' - during lesson
        - 'break' - during the break
        - 'ended' - after last lesson
    - call: call schedule
    - time: time to call
    - time_start: start time of the call
    - time_end: end time of the call
    """

    if not lessons:
        return None
    if calls is None:
        calls = api.timetable_call_schedule()
    if timestamp is None:
        timestamp = datetime.now()

    date = timestamp.date()

    # Filter only calls, which are in lessons
    lesson_numbers = [lesson['number'] for lesson in lessons]
    filtered_calls = [call for call in calls if call['number'] in lesson_numbers]

    # Parse calls time from string to datetime
    calls_time = []
    for call in filtered_calls:
        call_time_start = datetime.strptime(call['timeStart'], '%H:%M').time()
        call_time_end = datetime.strptime(call['timeEnd'], '%H:%M').time()

        calls_time.append({
            'timeStart': datetime.combine(date, call_time_start),
            'timeEnd': datetime.combine(date, call_time_end),
            'call': call,
        })

    # If lessons have not started
    first_call = calls_time[0]
    if timestamp < first_call['timeStart']:
        return {
            'status': 'not_started',
            'call': first_call['call'],
            'time': first_call['timeStart'] - timestamp,
            'time_start': first_call['timeStart'],
            'time_end': first_call['timeEnd'],
        }

    # If lessons is over
    last_call = calls_time[-1]
    if timestamp > last_call['timeEnd']:
        return {
            'status': 'ended',
            'call': last_call['call'],
            'time': timestamp - last_call['timeEnd'],
            'time_start': last_call['timeStart'],
            'time_end': last_call['timeEnd'],
        }

    # Get the current call
    for call in calls_time:
        if timestamp <= call['timeEnd']:
            cur_call = call
            break
    else:
        return None

    # If the break is going on
    if timestamp < cur_call['timeStart']:
        return {
            'status': 'break',
            'call': cur_call['call'],
            'time': cur_call['timeStart'] - timestamp,
            'time_start': cur_call['timeStart'],
            'time_end': cur_call['timeEnd'],
        }

    # If the lesson is going on
    return {
        'status': 'going',
        'call': cur_call['call'],
        'time': cur_call['timeEnd'] - timestamp,
        'time_start': cur_call['timeStart'],
        'time_end': cur_call['timeEnd'],
    }
