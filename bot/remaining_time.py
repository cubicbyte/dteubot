import telebot.types
from datetime import datetime, timedelta
from .settings import api

def get_remaining_time(message: telebot.types.Message, timestamp = datetime.now()) -> timedelta | None:
    """Returns the time before the start/end of the lesson"""

    schedule = api.timetable_group(message.config['groupId'], timestamp).json()
    date = timestamp.strftime('%Y-%m-%d')

    # if there are no lessons, return None
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

    return api.get_lesson(lessons)
