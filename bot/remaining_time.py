import telebot.types
from datetime import datetime, timedelta
from .settings import api

def get_remaining_time(message: telebot.types.Message, timestamp = datetime.now()) -> timedelta | None:
    '''
        Returns the time before the start/end of the lesson
        
        Positive value: time before the start
        Negative value: time until the end
    '''

    #return timedelta(days=1, hours=2, minutes=16, seconds=45)
    
    lesson_time = api.get_lesson()
    found = False
    start = 1 if lesson_time['status'] == 3 else 0

    for i in range(start, 7):
        schedule = api.timetable_group(message.config['schedule']['group_id'], timestamp + timedelta(days=i)).json()

        for day in schedule:
            if len(day['lessons']) != 0:
                found = True
                lessons = day
                break

        if found:
            break

    if not found:
        return None

    first_lesson_time = lesson_time['timetable_formatted'][lessons[0]['number']]['timeStart']
    cur_lesson_time = lesson_time['timetable_formatted'][lessons[lesson_time['lesson']]]['left']

    if timestamp < first_lesson_time:
        return lesson_time['time']

    return cur_lesson_time
