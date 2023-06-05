"""
Time formatter utility
"""

from datetime import timedelta
from settings import langs


def format_time(
        lang_code: str,
        time: timedelta,
        depth: int = 1) -> str:
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
        result += langs[lang_code]['text.time.short.hours']

    # Add {minutes}m.
    if cur_depth < depth and time >= timedelta(minutes=1):
        if cur_depth != 0:
            result += ' '
        cur_depth += 1
        result += str(time.seconds // 60 % 60)
        result += langs[lang_code]['text.time.short.minutes']

    # Add {seconds}s.
    if cur_depth < depth:
        if cur_depth != 0:
            result += ' '
        result += str(time.seconds % 60)
        result += langs[lang_code]['text.time.short.seconds']

    return result
