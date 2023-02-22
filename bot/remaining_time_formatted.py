from datetime import datetime
from .remaining_time import get_remaining_time
from .utils.format_time import format_time

def get_time(lang_code: str, groupId: int, timestamp = datetime.now()) -> dict:
    remaining_time = get_remaining_time(groupId, timestamp)

    if remaining_time is None:
        formatted = None
    else:
        formatted = format_time(lang_code, remaining_time['time'], depth=4)

    result = {
        'time': remaining_time,
        'formatted': formatted
    }

    return result
