"""
Utility functions for the bot
"""

import re
import time
from typing import Callable, List
from urllib.parse import parse_qsl

MAX_MESSAGE_LENGTH = 4096


def validate_bot_token(token: str) -> bool:
    """Validate bot token"""
    return re.fullmatch(r'\d+:[\w-]+', token) is not None


def array_split(array: list, row_size: int) -> list:
    """
    Split an array into rows

    Example:
    --------
    >>> array_split([1, 2, 3, 4, 5, 6], 2)
    [[1, 2], [3, 4], [5, 6]]
    """
    return [array[i:i + row_size] for i in range(0, len(array), row_size)]


def isint(string: any) -> bool:
    """Check if a string is an integer"""
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True


def isfloat(string: any) -> bool:
    """Check if a string is an float"""
    try:
        float(string)
    except ValueError:
        return False
    else:
        return True


def parse_callback_query(query: str) -> dict:
    """Parses a callback query string

    Example:
    >>> parse_callback_query('open.schedule.day#date=2004-06-12&somefield=somevalue')
    {
        'query': 'open.schedule.day',
        'args': {
            'date': '2004-06-12',
            'somefield': 'somevalue'
        }
    }
    """
    split = query.split('#')

    # If there are arguments, then parse them
    if len(split) != 1:
        args = dict(parse_qsl(split[1], keep_blank_values=True))
    else:
        args = {}

    return {
        'query': split[0],
        'args': args
    }


def clean_html(raw_html: str, tags_whitelist: list[str] | None = None) -> str:
    """Remove html tags from string"""

    # Save line breaks
    raw_html = raw_html.replace('<br>', '\n').replace('<br />', '\n')

    if tags_whitelist:
        tags = '|'.join(tags_whitelist)
        cleanr = re.compile(fr'<(?!\/?({tags})\b)[^>]*>', re.IGNORECASE)
    else:
        cleanr = re.compile('<.*?>')

    return re.sub(cleanr, '', raw_html)


def timeit(func: Callable | str = '?', print_result: bool = True):
    """
    Decorator for measuring execution time of a function

    Decorator usage:
    --------
    >>> @timeit
    ... def foo():
    ...     time.sleep(0.8)
    ...     return 42
    >>> foo()
    [foo] Execution time: 800.00 ms
    42

    Context manager usage:
    --------
    >>> with timeit('foo'):
    ...     time.sleep(0.8)
    [foo] Execution time: 800.00 ms
    """

    class _TimeitCtx:
        def __init__(self, name: str, print_result: bool = True) -> None:
            self.name = name
            self.print_result = print_result
            self.start = None
            self.end = None
            self.time = None

        def __enter__(self) -> None:
            self.start = time.time()
            return self

        def __exit__(self, *args) -> None:
            self.end = time.time()
            self.time = self.end - self.start

            if self.print_result:
                print(self)

        def __str__(self) -> str:
            return f'[{self.name}] Execution time: {self.time * 1000:.2f} ms'

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f'[{func.__name__}] Execution time: {(end - start) * 1000:.2f} ms')

        return result

    if isinstance(func, str):
        return _TimeitCtx(func, print_result)

    return wrapper


# Copied from the pyTelegramBotApi library
# https://github.com/eternnoir/pyTelegramBotAPI/blob/5d9a76b0dd0d3ee88c5c9d1329c06b24fdc4457b/telebot/util.py#L327
def smart_split(text: str, chars_per_string: int = MAX_MESSAGE_LENGTH) -> List[str]:
    r"""
    Splits one string into multiple strings, with a maximum
    amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.
    If `chars_per_string` > 4096: `chars_per_string` = 4096.
    Splits by '\n', '. ' or ' ' in exactly this priority.
    :param text: The text to split
    :type text: :obj:`str`
    :param chars_per_string: The number of maximum characters per part the text is split to.
    :type chars_per_string: :obj:`int`
    :return: The split text as a list of strings.
    :rtype: :obj:`list` of :obj:`str`
    """

    def _text_before_last(substr: str) -> str:
        return substr.join(part.split(substr)[:-1]) + substr

    chars_per_string = min(MAX_MESSAGE_LENGTH, chars_per_string)

    parts = []
    while True:
        if len(text) < chars_per_string:
            parts.append(text)
            return parts

        part = text[:chars_per_string]

        if "\n" in part:
            part = _text_before_last("\n")
        elif ". " in part:
            part = _text_before_last(". ")
        elif " " in part:
            part = _text_before_last(" ")

        parts.append(part)
        text = text[len(part):]
