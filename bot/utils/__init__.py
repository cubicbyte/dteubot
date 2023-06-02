import os
import re
import time
import json
from typing import Callable
from pathlib import Path
from urllib.parse import parse_qsl
from bot.schemas import Language


def array_split(array: list, row_size: int) -> list:
    """
    Split an array into rows

    Example:
    --------
    >>> array_split([1, 2, 3, 4, 5, 6], 2)
    [[1, 2], [3, 4], [5, 6]]
    """
    return [array[i:i + row_size] for i in range(0, len(array), row_size)]


def check_int(s: any) -> bool:
    """Check if a string is an integer"""
    if not isinstance(s, str):
        return False
    if s[0] == '-' or s[0] == '+':
        return s[1:].isdigit()
    return s.isdigit()


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
        args = dict(parse_qsl(split[1]))
    else:
        args = {}

    return {
        'query': split[0],
        'args': args
    }


def load_langs(dirpath: str) -> dict[str, Language]:
    """Load .json language files from directory"""

    langs = {}

    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        lang = load_lang_file(filepath)
        langs[lang.name] = lang

    return langs


def load_lang_file(filepath: str) -> Language:
    """Load .json language file"""

    lang_name = Path(filepath).stem

    with open(filepath, 'r', encoding='utf-8') as fp:
        lang = json.load(fp)

    return Language(lang, lang_name)


def clean_html(raw_html: str, tags_whitelist: list[str] = []) -> str:
    """Remove html tags from string"""

    if tags_whitelist:
        tags = '|'.join(tags_whitelist)
        cleanr = re.compile(fr'<(?!\/?({tags})\b)[^>]*>', re.IGNORECASE)
    else:
        cleanr = re.compile('<.*?>')

    return re.sub(cleanr, '', raw_html)


def timeit(func: Callable | str = '?'):
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

    class TimeitCtx:
        def __init__(self, name: str) -> None:
            self.name = name

        def __enter__(self) -> None:
            self.start = time.time()

        def __exit__(self, *args) -> None:
            end = time.time()
            print(f'[{self.name}] Execution time: {(end - self.start) * 1000:.2f} ms')

        def start(self) -> 'TimeitCtx':
            self.__enter__()
            return self
        
        def stop(self):
            self.__exit__()

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f'[{func.__name__}] Execution time: {(end - start) * 1000:.2f} ms')

        return result

    if type(func) == str:
        return TimeitCtx(func)
    else:
        return wrapper
