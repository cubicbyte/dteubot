import os
import logging
import requests.exceptions

from urllib.parse import urljoin
from datetime import timedelta
from requests_cache import CachedSession

logger = logging.getLogger()
session = CachedSession(
    'cache/groups',
    cache_control=True,
    expire_after=timedelta(days=7),
    allowable_methods=['GET', 'POST'],
    match_headers=True,
    stale_if_error=True
)

def get_groups(facultyId: int, course: int) -> list[dict[str, any]]:
    logger.debug('Getting groups list')

    req_data = {
        'facultyId': facultyId,
        'course': course
    }

    headers = {
        'Accept-Language': 'uk',
        'Content-Type': 'application/json; charset=utf-8'
    }

    url = urljoin(os.getenv('API_URL'), '/list/groups')
    timeout = int(os.getenv('API_REQUEST_TIMEOUT'))
    res = session.post(url, json=req_data, headers=headers, timeout=timeout)

    if not res.ok:
        raise requests.exceptions.HTTPError()

    return res
