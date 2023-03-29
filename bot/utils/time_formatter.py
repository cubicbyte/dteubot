from datetime import timedelta
from settings import langs

def format_time(lang_code: str, time: timedelta, depth = 1, short = True) -> str:
    """Formats timedelta into a readable format

    Example
    ----------
    >>> format_time('en', timedelta(days=2, hours=9, minutes=40, seconds=33), depth=2)
    '2d. 9h.'
    """

    result = ''
    cur_depth = 0

    if time >= timedelta(days=1):
        result += str(time.days) + ' ' + langs[lang_code]['text.time.short.days']
        cur_depth += 1

    if cur_depth < depth and time >= timedelta(hours=1):
        if cur_depth != 0:
            result += ' '
        cur_depth += 1
        result += str(time.seconds // 3600)
        if short:
            result += langs[lang_code]['text.time.short.hours']
        else:
            result += ' ' + langs[lang_code]['text.time.hours']

    if cur_depth < depth and time >= timedelta(minutes=1):
        if cur_depth != 0:
            result += ' '
        cur_depth += 1
        result += str(time.seconds // 60 % 60)
        if short:
            result += langs[lang_code]['text.time.short.minutes']
        else:
            result += ' ' + langs[lang_code]['text.time.minutes']

    if cur_depth < depth:
        if cur_depth != 0:
            result += ' '
        result += str(time.seconds % 60)
        if short:
            result += langs[lang_code]['text.time.short.seconds']
        else:
            result += ' ' + langs[lang_code]['text.time.seconds']

    return result
