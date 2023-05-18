from urllib.parse import parse_qsl


def array_split(array: list, row_size: int) -> list:
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
