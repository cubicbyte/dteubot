"""
Time formatter utility
"""

from datetime import timedelta
from settings import langs


def format_time(
        lang_code: str,
        time: timedelta,
        depth: int = 1,
        short: bool = True) -> str:
    """Formats timedelta into a readable format

    Example
    ----------
    >>> format_time('en', timedelta(days=2, hours=9, minutes=40, seconds=33), depth=2)
    '2d. 9h.'
    """

    result = ''
    cur_depth = 0

    # Add {days}d.
    if time >= timedelta(days=1):
        result += str(time.days) + ' ' + langs[lang_code]['text.time.short.days']
        cur_depth += 1

    # Add {hours}h.
    if cur_depth < depth and time >= timedelta(hours=1):
        if cur_depth != 0:
            result += ' '
        cur_depth += 1
        result += str(time.seconds // 3600)
        if short:
            result += langs[lang_code]['text.time.short.hours']
        else:
            result += ' ' + langs[lang_code]['text.time.hours']

    # Add {minutes}m.
    if cur_depth < depth and time >= timedelta(minutes=1):
        if cur_depth != 0:
            result += ' '
        cur_depth += 1
        result += str(time.seconds // 60 % 60)
        if short:
            result += langs[lang_code]['text.time.short.minutes']
        else:
            result += ' ' + langs[lang_code]['text.time.minutes']

    # Add {seconds}s.
    if cur_depth < depth:
        if cur_depth != 0:
            result += ' '
        result += str(time.seconds % 60)
        if short:
            result += langs[lang_code]['text.time.short.seconds']
        else:
            result += ' ' + langs[lang_code]['text.time.seconds']

    return result
