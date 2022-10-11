import os
import logging
import requests.exceptions

from requests import Response
from urllib.parse import urljoin
from datetime import timedelta
from requests_cache import CachedSession



logger = logging.getLogger()
session = CachedSession(
    'cache/calls-schedule',
    cache_control=True,
    expire_after=timedelta(days=7),
    allowable_methods=['POST'],
    match_headers=True,
    stale_if_error=True
)



def get_calls_schedule() -> Response:
    logger.debug('Getting calls schedule')

    headers = {
        'Accept-Language': 'uk',
        'Content-Type': 'application/json; charset=utf-8'
    }

    url = urljoin(os.getenv('API_URL'), '/time-table/call-schedule')
    timeout = int(os.getenv('API_REQUEST_TIMEOUT'))
    res = session.post(url, headers=headers, timeout=timeout)

    if not res.ok:
        raise requests.exceptions.HTTPError()

    return res
