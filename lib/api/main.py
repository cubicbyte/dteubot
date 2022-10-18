import logging
import requests.exceptions

from requests import Response
from urllib.parse import urljoin
from datetime import datetime, timedelta
from requests_cache import CachedSession

logger = logging.getLogger(__name__)
logger.info('Initializing api')

session = CachedSession(
    'cache/api',
    cache_control=True,
    expire_after=timedelta(days=1),
    allowable_methods=['GET', 'POST'],
    match_headers=True,
    stale_if_error=True
)



class Api:
    def __init__(self, url: str, timeout: int = None) -> None:
        logger.info('Creating Api instance with url %s' % url)
        self.url = url
        self.timeout = timeout

    def get_schedule(self, groupId: int, date = datetime.today()) -> Response:
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)

        req_data = {
            'groupId': groupId,
            'dateStart': week_start.strftime('%Y-%m-%d'),
            'dateEnd': week_end.strftime('%Y-%m-%d')
        }

        logger.debug(f'Getting schedule. groupId: {groupId}, date: {req_data["dateStart"]}')

        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, '/time-table/group')
        res = session.post(url, json=req_data, headers=headers, timeout=self.timeout)

        if not res.ok:
            raise requests.exceptions.HTTPError()

        return res

    def get_groups(self, facultyId: int, course: int) -> Response:
        logger.debug(f'Getting groups list. facultyId: {facultyId}, course: {course}')

        req_data = {
            'facultyId': facultyId,
            'course': course
        }

        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, '/list/groups')
        res = session.post(url, json=req_data, headers=headers, timeout=self.timeout)

        if not res.ok:
            raise requests.exceptions.HTTPError()

        return res

    def get_courses(self, facultyId: int) -> Response:
        logger.debug(f'Getting courses list. facultyId: {facultyId}')

        req_data = {
            'facultyId': facultyId
        }

        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, '/list/courses')
        res = session.post(url, json=req_data, headers=headers, timeout=self.timeout)

        if not res.ok:
            raise requests.exceptions.HTTPError()

        return res

    def get_faculties(self, structureId: int) -> Response:
        logger.debug(f'Getting faculties list. structureId: {structureId}')

        req_data = {
            'structureId': structureId
        }

        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, '/list/faculties')
        res = session.post(url, json=req_data, headers=headers, timeout=self.timeout)

        if not res.ok:
            raise requests.exceptions.HTTPError()

        return res

    def get_structures(self) -> Response:
        logger.debug('Getting structures list')

        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, '/list/structures')
        res = session.get(url, headers=headers, timeout=self.timeout)

        if not res.ok:
            raise requests.exceptions.HTTPError()

        return res

    def get_calls_schedule(self) -> Response:
        logger.debug('Getting calls schedule')

        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, '/time-table/call-schedule')
        res = session.post(url, headers=headers, timeout=self.timeout)

        if not res.ok:
            raise requests.exceptions.HTTPError()

        return res
