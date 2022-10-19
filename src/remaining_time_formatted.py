import telebot.types
from datetime import datetime
from .remaining_time import get_remaining_time
from .format_time import format_time

def get_time(message: telebot.types.Message, timestamp = datetime.now()) -> dict:
    remaining_time = get_remaining_time(message, timestamp)

    if remaining_time is None:
        formatted = None
    else:
        formatted = format_time(message, remaining_time, depth=4)

    result = {
        'time': remaining_time,
        'formatted': formatted
    }

    return result
