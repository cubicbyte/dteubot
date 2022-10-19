import telebot.types
from datetime import timedelta

def format_time(message: telebot.types.Message, time: timedelta, depth = 1) -> str:
    result = ''
    cur_depth = 0

    if time >= timedelta(days=1):
        result += str(time.days) + ' ' + message.lang['text']['days_short']
        cur_depth += 1

    if cur_depth < depth and time >= timedelta(hours=1):
        result += ' ' + str(time.seconds // 3600) + ' ' + message.lang['text']['hours_short']
        cur_depth += 1

    if cur_depth < depth and time >= timedelta(minutes=1):
        result += ' ' + str(time.seconds // 60 % 60) + ' ' + message.lang['text']['minutes_short']
        cur_depth += 1

    if cur_depth < depth:
        result += ' ' + str(time.seconds % 60) + ' ' + message.lang['text']['seconds_short']

    return result
