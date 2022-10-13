import logging

from urllib.parse import urljoin
from datetime import timedelta
from requests_cache import CachedSession

logger = logging.getLogger('api')

class Api:
    __session = CachedSession(
        'cache/api',
        cache_control=True,
        expire_after=timedelta(days=1),
        allowable_methods=['GET', 'POST'],
        match_headers=True,
        stale_if_error=True
    )

    def __init__(self, url: str) -> None:
        self.url = url

    