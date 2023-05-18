import os
import json
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
