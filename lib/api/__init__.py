
# API docs can be found at https://mkr.org.ua/portal-api-docs.html

import logging
import pytz

logger = logging.getLogger(__name__)
logger.info('Initializing api module')

from urllib.parse import urljoin
from datetime import date, datetime
from requests_cache import CachedSession, Response
from .utils.date_range import get_date_range



class Api:
    def __init__(self, url: str, timeout: int = None, **kwargs) -> None:
        logger.info('Creating Api instance with url %s' % url)
        self.url = url
        self._timeout = timeout
        self._session = CachedSession(
            cache_name='cache/api',
            cache_control=True,
            allowable_methods=['GET', 'POST'],
            match_headers=True,
            stale_if_error=True,
            **kwargs
        )

    def _make_request(self, path: str, method: str = 'GET', json: dict = None, *args, **kwargs) -> Response:
        logger.debug(f'Making {method} request to {path} with JSON data {json}')
        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, path)
        res = self._session.request(method, url, headers=headers, json=json, timeout=self._timeout, *args, **kwargs)
        res.raise_for_status()

        return res



    # /time-table
    def timetable_group(self, groupId: int, date: date) -> Response:
        """Returns the schedule for the group"""
        date_range = get_date_range(date)

        return self._make_request('/time-table/group', 'POST', json={
            'groupId': groupId,
            'dateStart': date_range[0].strftime('%Y-%m-%d'),
            'dateEnd': date_range[1].strftime('%Y-%m-%d')
        })

    def timetable_student(self, studentId: int, date: date) -> Response:
        """Returns the schedule for the student"""
        date_range = get_date_range(date)

        return self._make_request('/time-table/student', 'POST', json={
            'studentId': studentId,
            'dateStart': date_range[0].strftime('%Y-%m-%d'),
            'dateEnd': date_range[1].strftime('%Y-%m-%d')
        })

    def timetable_teacher(self, teacherId: int, date: date) -> Response:
        """Returns the schedule for the teacher"""
        date_range = get_date_range(date)

        return self._make_request('/time-table/teacher', 'POST', json={
            'teacherId': teacherId,
            'dateStart': date_range[0].strftime('%Y-%m-%d'),
            'dateEnd': date_range[1].strftime('%Y-%m-%d')
        })

    def timetable_classroom(self, classroomId: int, date: date) -> Response:
        """Returns audience schedule (when and what groups are in it)"""
        date_range = get_date_range(date)

        return self._make_request('/time-table/classroom', 'POST', json={
            'classroomId': classroomId,
            'dateStart': date_range[0].strftime('%Y-%m-%d'),
            'dateEnd': date_range[1].strftime('%Y-%m-%d')
        })

    def timetable_universal(self, date: date):
        """Returns whole university schedule"""
        return self._make_request('/time-table/universal', 'POST', json={
            'date': date.strftime('%Y-%m-%d')
        })

    def timetable_call(self) -> Response:
        """Returns the call schedule"""
        return self._make_request('/time-table/call-schedule', 'POST')

    def timetable_ad(self, classCode: int, date: str) -> Response:
        """Returns an announcement for the current lesson\n
        Usually contains a lesson link in Teams/Zoom"""
        return self._make_request('/time-table/schedule-ad', 'POST', json={
            'r1': classCode,
            'r2': date
        })

    def timetable_free_classrooms(self, structureId: int, corpusId: int, lessonNumberStart: int, lessonNumberEnd: int, datetime: datetime):
        """Returns list of free classrooms"""
        return self._make_request('/time-table/free-classroom', 'POST', json={
            'structureId': structureId,
            'corpusId': corpusId,
            'lessonNumberStart': lessonNumberStart,
            'lessonNumberEnd': lessonNumberEnd,
            'date': datetime.astimezone(pytz.UTC).isoformat(sep='T', timespec='milliseconds') + 'Z'
        })
    

    # /list
    def list_structures(self) -> Response:
        """Returns list of structures"""
        return self._make_request('/list/structures')

    def list_faculties(self, structureId: int) -> Response:
        """Returns list of faculties"""
        return self._make_request('/list/faculties', 'POST', json={
            'structureId': structureId
        })

    def list_courses(self, facultyId: int) -> Response:
        """Returns list of courses"""
        return self._make_request('/list/courses', 'POST', json={
            'facultyId': facultyId
        })

    def list_groups(self, facultyId: int, course: int) -> Response:
        """Return list of groups"""
        return self._make_request('/list/groups', 'POST', json={
            'facultyId': facultyId,
            'course': course
        })

    def list_chairs(self, structureId: int, facultyId: int) -> Response:
        """Returns list of chairs"""
        return self._make_request('/list/chairs', 'POST', json={
            'structureId': structureId,
            'facultyId': facultyId
        })
    
    def list_teachers_by_chair(self, chairId: int) -> Response:
        """Returns a list of teachers from the given chair"""
        return self._make_request('/list/teachers-by-chair', 'POST', json={
            'chairId': chairId
        })

    def list_students_by_group(self, groupId: int) -> Response:
        """Returns a list of students from the given group"""
        return self._make_request('/list/students-by-group', 'POST', json={
            'groupId': groupId
        })



    # /other
    def search_teacher(self, name: str) -> Response:
        """Looking for a teacher by a fragment of his last name only\n
        Not case sensitive, returns an array of the first 50 teachers found"""
        return self._make_request('/other/search-teachers', 'POST', json={
            'name': name
        })
