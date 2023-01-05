import telebot.types
from datetime import timedelta

def format_time(message: telebot.types.Message, time: timedelta, depth = 1) -> str:
    """Formats timedelta into a readable format
    
    Example
    ----------
    >>> format_time(message, timedelta(days=2, hours=9, minutes=40, seconds=33), depth=2)
    '1d. 2h.'
    """

    result = ''
    cur_depth = 0

    if time >= timedelta(days=1):
        result += str(time.days) + ' ' + message.lang['text.time.short.days']
        cur_depth += 1

    if cur_depth < depth and time >= timedelta(hours=1):
        result += ' ' + str(time.seconds // 3600) + ' ' + message.lang['text.time.short.hours']
        cur_depth += 1

    if cur_depth < depth and time >= timedelta(minutes=1):
        result += ' ' + str(time.seconds // 60 % 60) + ' ' + message.lang['text.time.short.minutes']
        cur_depth += 1

    if cur_depth < depth:
        result += ' ' + str(time.seconds % 60) + ' ' + message.lang['text.time.short.seconds']

    return result
