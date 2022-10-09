import telebot.types

from datetime import datetime, timedelta
from .get_schedule import get_schedule

def get_remaining_time(message: telebot.types.Message, timestamp = datetime.now()) -> timedelta | None:
    '''
        Returns the time before the start/end of the lesson
        
        Positive value: time before the start
        Negative value: time until the end
    '''

#    date = datetime.today()
#    found = False
#
#    for i in range(7):
#        res = get_schedule(message, date)
#        schedule = res.json()
#
#        for day in schedule:
#            if len(day['lessons']) != 0:
#                found = True
#                break
#
#            date += timedelta(days=1)
#
#    if not found:
#        return None
#
#    lesson = schedule['lessons'][0]


    return timedelta(days=1, hours=2, minutes=16, seconds=45)

    return {
        'to': None,
        'remaining': None
    }
    
    day_i = str(date.weekday())

    if week_number == None or not message.schedule_valid:
        return {
            'to': None,
            'remaining': None
        }

    schedule = get_schedule(message)
    week = schedule['weeks'][week_number - 1]

    if not day_i in week:
        return {
            'to': None,
            'remaining': None
        }

    day = week[day_i]

    if len(day.keys()) == 0:
        return {
            'to': None,
            'remaining': None
        }

    classes = []

    for class_number in day.keys():
        ring = rings_schedule[int(class_number) - 1]
        classes.append({
            'from': datetime.fromisoformat(date.strftime(f'%Y-%m-%d {ring["from"]}')),
            'to': datetime.fromisoformat(date.strftime(f'%Y-%m-%d {ring["to"]}'))
        })
        
    if date >= classes[-1]['to']:
        return {
            'to': None,
            'remaining': None
        }

    if date < classes[0]['from']:
        return {
            'to': 0,
            'remaining': classes[0]['from'] - date
        }

    for i in classes:
        if date < i['to']:
            if date > i['from']:
                return {
                    'to': 1,
                    'remaining': i['to'] - date
                }

            return {
                'to': 0,
                'remaining': i['from'] - date
            }

    return {
        'to': None,
        'remaining': None
    }
