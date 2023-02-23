
# API docs can be found at https://mkr.org.ua/portal-api-docs.html

import logging
import pytz

logger = logging.getLogger(__name__)
logger.info('Initializing api module')

from urllib.parse import urljoin
from datetime import timedelta, datetime, date as _date
from requests_cache import CachedSession



class Api:
    def __init__(self, url: str, timeout: int = None, **kwargs) -> None:
        logger.info('Creating Api instance with url %s' % url)
        self.url = url
        self._timeout = timeout
        self._session = CachedSession(
            cache_name='cache/http-cache',
            cache_control=True,
            allowable_methods=['GET', 'POST'],
            match_headers=True,
            stale_if_error=True,
            **kwargs
        )

    def _make_request(self, path: str, method: str = 'GET', json: dict = None, *args, **kwargs) -> any:
        logger.debug(f'Making {method} request to {path} with JSON data {json}')
        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, path)
        res = self._session.request(method, url, headers=headers, json=json, timeout=self._timeout, *args, **kwargs)
        res.raise_for_status()

        return res.json()



    # /time-table
    def timetable_group(self, groupId: int, dateStart: _date | str, dateEnd: _date | str = None) -> list[dict]:
        """Returns the schedule for the group"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return self._make_request('/time-table/group', 'POST', json={
            'groupId': groupId,
            'dateStart': dateStart,
            'dateEnd': dateEnd
        })

    def timetable_student(self, studentId: int, dateStart: _date | str, dateEnd: _date | str = None) -> list[dict]:
        """Returns the schedule for the student"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return self._make_request('/time-table/student', 'POST', json={
            'studentId': studentId,
            'dateStart': dateStart,
            'dateEnd': dateEnd
        })

    def timetable_teacher(self, teacherId: int, dateStart: _date | str, dateEnd: _date | str = None) -> list[dict]:
        """Returns the schedule for the teacher"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return self._make_request('/time-table/teacher', 'POST', json={
            'teacherId': teacherId,
            'dateStart': dateStart,
            'dateEnd': dateEnd
        })

    def timetable_classroom(self, classroomId: int, dateStart: _date | str, dateEnd: _date | str = None) -> list[dict]:
        """Returns audience schedule (when and what groups are in it)"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return self._make_request('/time-table/classroom', 'POST', json={
            'classroomId': classroomId,
            'dateStart': dateStart.strftime('%Y-%m-%d'),
            'dateEnd': dateEnd.strftime('%Y-%m-%d')
        })

    def timetable_universal(self, date: _date | str) -> list[dict]:
        """Returns whole university schedule"""
        if type(date) == _date:
            date = date.strftime('%Y-%m-%d')
        return self._make_request('/time-table/universal', 'POST', json={
            'date': date
        })

    def timetable_call(self) -> list[dict]:
        """Returns the call schedule"""
        return self._make_request('/time-table/call-schedule', 'POST')

    def timetable_ad(self, classCode: int, date: _date | str) -> list[dict]:
        """Returns an announcement for the current lesson\n
        Usually contains a lesson link in Teams/Zoom"""
        if type(date) == _date:
            date = date.strftime('%Y-%m-%d')
        return self._make_request('/time-table/schedule-ad', 'POST', json={
            'r1': classCode,
            'r2': date
        })

    def timetable_free_classrooms(self, structureId: int, corpusId: int, lessonNumberStart: int, lessonNumberEnd: int, date: datetime | str) -> list[dict]:
        """Returns list of free classrooms
        Date format: `2023-02-23T10:26:00.000Z` or `datetime.datetime`"""
        if type(date) == datetime:
            date = date.astimezone(pytz.UTC).isoformat(sep='T', timespec='milliseconds') + 'Z'
        return self._make_request('/time-table/free-classroom', 'POST', json={
            'structureId': structureId,
            'corpusId': corpusId,
            'lessonNumberStart': lessonNumberStart,
            'lessonNumberEnd': lessonNumberEnd,
            'date': date
        })



    # /list
    def list_structures(self) -> list[dict]:
        """Returns list of structures"""
        return self._make_request('/list/structures')

    def list_faculties(self, structureId: int) -> list[dict]:
        """Returns list of faculties"""
        return self._make_request('/list/faculties', 'POST', json={
            'structureId': structureId
        })

    def list_courses(self, facultyId: int) -> list[dict]:
        """Returns list of courses"""
        return self._make_request('/list/courses', 'POST', json={
            'facultyId': facultyId
        })

    def list_groups(self, facultyId: int, course: int) -> list[dict]:
        """Return list of groups"""
        return self._make_request('/list/groups', 'POST', json={
            'facultyId': facultyId,
            'course': course
        })

    def list_chairs(self, structureId: int, facultyId: int) -> list[dict]:
        """Returns list of chairs"""
        return self._make_request('/list/chairs', 'POST', json={
            'structureId': structureId,
            'facultyId': facultyId
        })

    def list_teachers_by_chair(self, chairId: int) -> list[dict]:
        """Returns a list of teachers from the given chair"""
        return self._make_request('/list/teachers-by-chair', 'POST', json={
            'chairId': chairId
        })

    def list_students_by_group(self, groupId: int) -> list[dict]:
        """Returns a list of students from the given group"""
        return self._make_request('/list/students-by-group', 'POST', json={
            'groupId': groupId
        })



    # /other
    def search_teacher(self, name: str) -> list[dict]:
        """Looking for a teacher by a fragment of his last name only\n
        Not case sensitive, returns an array of the first 50 teachers found"""
        return self._make_request('/other/search-teachers', 'POST', json={
            'name': name
        })


import json
from ..cache_reader import CacheReader
class CachedApi(Api):
    def __init__(self, url: str, timeout: int = None, enable_http = False, **kwargs):
        super().__init__(url, timeout, **kwargs)
        self._http_enabled = enable_http
        self._cache = CacheReader('cache/mkr-cache.sqlite')

    def timetable_group(self, groupId: int, dateStart: _date, dateEnd: _date = None) -> list[dict]:
        if dateEnd is None:
            dateEnd = dateStart + timedelta(days=6)
        res = self._cache.get_schedule(groupId, dateStart, dateEnd)
        if res is None:
            if self.__http_enabled:
                res = super().timetable_group(groupId, dateStart, dateEnd)
            else: res = []
        else:
            _res = res
            res = []
            for day in _res:
                res.append({
                    'date': day[1],
                    'lessons': json.loads(day[2])
                })
        return res

    def list_structures(self) -> list[dict]:
        data = self._cache.get_structures()
        res = list({
            'id': i[0],
            'shortName': i[1],
            'fullName': i[2]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_structures()
            else: res = []
        return res

    def list_faculties(self, structureId: int) -> list[dict]:
        data = self._cache.get_faculties(structureId)
        res = list({
            'id': i[1],
            'shortName': i[2],
            'fullName': i[3]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_faculties(structureId)
            else: res = []
        return res

    def list_courses(self, facultyId: int) -> list[dict]:
        data = self._cache.get_courses(facultyId)
        res = list({
            'course': i[1]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_courses(facultyId)
            else: res = []
        return res

    def list_groups(self, facultyId: int, course: int) -> list[dict]:
        data = self._cache.get_groups(facultyId, course)
        res = list({
            'id': i[1],
            'name': i[2],
            'course': i[3],
            'priority': i[4],
            'educationForm': i[5]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_groups(facultyId, course)
            else: res = []
        return res
