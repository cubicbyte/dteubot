from urllib.parse import parse_qsl

def parse_callback_query(query: str) -> dict:
    split = query.split('#')

    if len(split) != 1:
        args = dict(parse_qsl(split[1]))
    else:
        args = {}
        if '=' in query:
            split = query.split('=')

            # TODO: remove this after some time
            if split[0] == 'open.schedule.day':
                args = {
                    'date': split[1]
                }

    return {
        'query': split[0],
        'args': args
    }
