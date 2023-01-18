from urllib.parse import parse_qsl

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

    # If there is 
    if len(split) != 1:
        args = dict(parse_qsl(split[1]))
    else:
        args = {}

        # TODO: remove code below after some time
        if '=' in query:
            split = query.split('=')
            if split[0] == 'open.schedule.day':
                args = {
                    'date': split[1]
                }

    return {
        'query': split[0],
        'args': args
    }
