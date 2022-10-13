import telebot.types

from datetime import datetime, timedelta
from .get_schedule import get_schedule
from .get_calls_schedule import get_calls_schedule

def get_remaining_time(message: telebot.types.Message, timestamp = datetime.now()) -> timedelta | None:
    '''
        Returns the time before the start/end of the lesson
        
        Positive value: time before the start
        Negative value: time until the end
    '''

    return timedelta(days=1, hours=2, minutes=16, seconds=45)
    
    date = datetime.today()
    found = False

    for i in range(7):
        res = get_schedule(message.config['schedule']['group_id'], date)
        schedule = res.json()

        for day in schedule:
            if len(day['lessons']) != 0:
                found = True
                break

            date += timedelta(days=1)

    if not found:
        return None

    lesson = schedule['lessons'][0]


