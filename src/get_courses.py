import os
import logging
import requests.exceptions

from urllib.parse import urljoin
from datetime import timedelta
from requests_cache import CachedSession

logger = logging.getLogger()
session = CachedSession(
    'groups_cache',
    cache_control=True,
    expire_after=timedelta(days=7),
    allowable_methods=['GET', 'POST'],
    match_headers=True,
    stale_if_error=True
)

def get_courses(structureId: int, facultyId: int) -> list[dict[str, any]]:
    logger.debug('Getting courses list')

    req_data = {
        'structureId': structureId,
        'facultyId': facultyId
    }

    headers = {
        'Accept-Language': 'uk',
        'Content-Type': 'application/json; charset=utf-8'
    }

    url = urljoin(os.getenv('API_URL'), '/list/courses')
    timeout = int(os.getenv('API_REQUEST_TIMEOUT'))
    res = session.post(url, json=req_data, headers=headers, timeout=timeout)

    if not res.ok:
        raise requests.exceptions.HTTPError()

    return res
