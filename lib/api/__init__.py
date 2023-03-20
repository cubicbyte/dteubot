
# API docs can be found at https://mkr.org.ua/portal-api-docs.html

import os.path
import logging
import pytz

from typing import List
from datetime import timedelta, datetime, date as _date
from urllib.parse import urljoin
from requests_cache import CachedSession, DEFAULT_CACHE_NAME
from .schemas import *

logger = logging.getLogger(__name__)
logger.info('Initializing api module')



class Api:
    VERSION = '1.6.1'

    def __init__(self, url: str, timeout: int = None, **kwargs) -> None:
        logger.info('Creating Api instance with url %s' % url)
        self.url = url
        self._timeout = timeout
        self._session = CachedSession(
            cache_control=True,
            allowable_methods=['GET', 'POST'],
            match_headers=True,
            stale_if_error=True,
            **kwargs
        )

    def _make_request(self, path: str, method: str = 'GET', json: dict = None, raw = False, *args, **kwargs) -> any:
        logger.debug(f'Making {method} request to {path} with JSON data {json}')
        headers = {
            'Accept-Language': 'uk',
            'Content-Type': 'application/json; charset=utf-8'
        }

        url = urljoin(self.url, path)
        res = self._session.request(method, url, headers=headers, json=json, timeout=self._timeout, *args, **kwargs)
        res.raise_for_status()

        if raw:
            return res
        return res.json()


    # /time-table
    def timetable_group(self, groupId: int, dateStart: _date | str, dateEnd: _date | str = None, *req_args, **req_kwargs) -> List[TimeTableDate]:
        """Returns the schedule for the group"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return TimeTableDate.from_json(self._make_request('/time-table/group', 'POST', json={
            'groupId': groupId,
            'dateStart': dateStart,
            'dateEnd': dateEnd
        }, *req_args, **req_kwargs))


    def timetable_student(self, studentId: int, dateStart: _date | str, dateEnd: _date | str = None, *req_args, **req_kwargs) -> List[TimeTableDate]:
        """Returns the schedule for the student"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return TimeTableDate.from_json(self._make_request('/time-table/student', 'POST', json={
            'studentId': studentId,
            'dateStart': dateStart,
            'dateEnd': dateEnd
        }, *req_args, **req_kwargs))

    def timetable_teacher(self, teacherId: int, dateStart: _date | str, dateEnd: _date | str = None, *req_args, **req_kwargs) -> List[TimeTableDate]:
        """Returns the schedule for the teacher"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return TimeTableDate.from_json(self._make_request('/time-table/teacher', 'POST', json={
            'teacherId': teacherId,
            'dateStart': dateStart,
            'dateEnd': dateEnd
        }, *req_args, **req_kwargs))

    def timetable_classroom(self, classroomId: int, dateStart: _date | str, dateEnd: _date | str = None, *req_args, **req_kwargs) -> List[TimeTableDate]:
        """Returns audience schedule (when and what groups are in it)"""
        if type(dateStart) == _date:
            dateStart = dateStart.strftime('%Y-%m-%d')
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.strftime('%Y-%m-%d')
        return TimeTableDate.from_json(self._make_request('/time-table/classroom', 'POST', json={
            'classroomId': classroomId,
            'dateStart': dateStart.strftime('%Y-%m-%d'),
            'dateEnd': dateEnd.strftime('%Y-%m-%d')
        }, *req_args, **req_kwargs))

    def timetable_call_schedule(self, *req_args, **req_kwargs) -> List[CallSchedule]:
        """Returns the call schedule"""
        return CallSchedule.from_json(self._make_request('/time-table/call-schedule', 'POST', *req_args, **req_kwargs))

    def timetable_ad(self, classCode: int, date: _date | str, *req_args, **req_kwargs) -> Rd:
        """Returns an announcement for the current lesson\n
        Usually contains a lesson link in Teams/Zoom"""
        if type(date) == _date:
            date = date.strftime('%Y-%m-%d')
        return Rd.from_json(self._make_request('/time-table/schedule-ad', 'POST', json={
            'r1': classCode,
            'r2': date
        }, *req_args, **req_kwargs))

    def timetable_free_classrooms(self, structureId: int, corpusId: int, lessonNumberStart: int, lessonNumberEnd: int, date: datetime | str, *req_args, **req_kwargs) -> List[Classroom]:
        """Returns list of free classrooms
        Date format: `2023-02-23T10:26:00.000Z` or `datetime.datetime`"""
        if type(date) == datetime:
            date = date.astimezone(pytz.UTC).isoformat(sep='T', timespec='milliseconds') + 'Z'
        return Classroom.from_json(self._make_request('/time-table/free-classroom', 'POST', json={
            'structureId': structureId,
            'corpusId': corpusId,
            'lessonNumberStart': lessonNumberStart,
            'lessonNumberEnd': lessonNumberEnd,
            'date': date
        }, *req_args, **req_kwargs))


    # /list
    def list_structures(self, *req_args, **req_kwargs) -> List[Structure]:
        """Returns list of structures"""
        return Structure.from_json(self._make_request('/list/structures', *req_args, **req_kwargs))

    def list_faculties(self, structureId: int, *req_args, **req_kwargs) -> List[Faculty]:
        """Returns list of faculties"""
        return Faculty.from_json(self._make_request('/list/faculties', 'POST', json={
            'structureId': structureId
        }, *req_args, **req_kwargs))

    def list_courses(self, facultyId: int, *req_args, **req_kwargs) -> List[Course]:
        """Returns list of courses"""
        return Course.from_json(self._make_request('/list/courses', 'POST', json={
            'facultyId': facultyId
        }, *req_args, **req_kwargs))

    def list_groups(self, facultyId: int, course: int, *req_args, **req_kwargs) -> List[Group]:
        """Return list of groups"""
        return Group.from_json(self._make_request('/list/groups', 'POST', json={
            'facultyId': facultyId,
            'course': course
        }, *req_args, **req_kwargs))

    def list_chairs(self, structureId: int, facultyId: int, *req_args, **req_kwargs) -> List[Chair]:
        """Returns list of chairs"""
        return Chair.from_json(self._make_request('/list/chairs', 'POST', json={
            'structureId': structureId,
            'facultyId': facultyId
        }, *req_args, **req_kwargs))

    def list_teachers_by_chair(self, chairId: int, *req_args, **req_kwargs) -> List[Person]:
        """Returns a list of teachers from the given chair"""
        return Person.from_json(self._make_request('/list/teachers-by-chair', 'POST', json={
            'chairId': chairId
        }, *req_args, **req_kwargs))

    def list_students_by_group(self, groupId: int, *req_args, **req_kwargs) -> List[Student]:
        """Returns a list of students from the given group"""
        return Student.from_json(self._make_request('/list/students-by-group', 'POST', json={
            'groupId': groupId
        }, *req_args, **req_kwargs))


    # /other
    def search_teacher(self, name: str, *req_args, **req_kwargs) -> List[TeacherByName]:
        """Looking for a teacher by a fragment of his last name only\n
        Not case sensitive, returns an array of the first 50 teachers found"""
        return TeacherByName.from_json(self._make_request('/other/search-teachers', 'POST', json={
            'name': name
        }, *req_args, **req_kwargs))


    # General
    def icon(self, *req_args, **req_kwargs) -> bytes:
        """Returns the university logo"""
        return self._make_request('/icon', raw=True, *req_args, **req_kwargs).content

    def version(self, *req_args, **req_kwargs) -> Version:
        """Returns the version of the API"""
        return Version.from_json(self._make_request('/version', *req_args, **req_kwargs))


    # Not implemented
    def timetable_universal(self, date: _date | str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def user_info2(self, id: int, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def user_info(self, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def user_change_password(self, password: str, newPassword: str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def user_change_password2(self, id: int, newPassword: str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def user_delete(self, id: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def user_update2(self, id: int, blocked: int, username: str, email: str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def user_update(self, username: str, email: str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def user_create(self, id: int, type: int, username: str, email: str, password: str, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def user_search_student(self, code: int, birthday: _date | str, type: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def user_search_teacher(self, inn: str, birthday: _date | str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def user_change_account(self, type: int, id: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def user_change_account2(self, id: int, type: int, newId: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def inquiry_types(self, facultyId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def journal_student(self, year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def journal_full_discipline_journal(self, disciplineId: int, type: int, year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_students(self, lastId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def student_semester_list(self, onlyActive: bool, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def student_info(self, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def student_search_by_email(self, email: str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def student_search(self, lastName: str, facultyId: int, specialityFullName: str, course: int, groupName: str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def docs_get_new_docs(self, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def docs_mark_docs_as_read(self, docs: List[int], *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def docs_get_docs_on_control(self, countDays: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_dols(self, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_structures(self, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_faculties(self, structureId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_chairs(self, structureId: int, facultyId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_teacher_identifiers(self, lastId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_chair_info(self, chairIds: List[int], *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_group_info(self, groupIds: List[int], *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_students(self, lastId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_teachers(self, lastId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def org_set_external_ids(self, externalIds: List[dict], *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def login(self, username: str, password: str, app_key: str, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def auth_data(self, username: str, password: str, key: str, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError
    def academ_disciplines(self, lastId: int, year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def academ_learning_plans(self, disciplineIds: List[int], year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def exam_sheets(self, year: int, semester: int, educationDisciplineId: int, groupId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def exam_statement_list(self, year: int, semester: int, educationDisciplineId: int, groupId: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError
    def exam_set_date_enter(self, sheetId: int, dateEnter: _date | str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def exam_close(self, sheetId: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError
    def exam_set_marks(self, sheetId: int, marks: List[dict], *req_args, **req_kwargs) -> None:
        raise NotImplementedError


import json
from ..cache_reader import CacheReader
class CachedApi(Api):
    def __init__(self, url: str, timeout: int = None, enable_http = False, **kwargs):
        super().__init__(url, timeout, **kwargs)
        cache_name = DEFAULT_CACHE_NAME if not 'cache_name' in kwargs else kwargs['cache_name']
        cache_path = os.path.join(os.path.dirname(cache_name), 'mkr-cache.sqlite')
        self._http_enabled = enable_http
        self._cache = CacheReader(cache_path)

    def timetable_group(self, groupId: int, dateStart: _date, dateEnd: _date = None, *req_args, **req_kwargs) -> List[TimeTableDate]:
        if dateEnd is None:
            dateEnd = dateStart + timedelta(days=6)
        res = self._cache.get_schedule(groupId, dateStart, dateEnd)
        if res is None:
            if self.__http_enabled:
                res = super().timetable_group(groupId, dateStart, dateEnd, *req_args, **req_kwargs)
            else: res = []
        else:
            _res = res
            res = []
            for day in _res:
                res.append({
                    'date': day[1],
                    'lessons': json.loads(day[2])
                })
        return TimeTableDate.from_json(res)

    def list_structures(self, *req_args, **req_kwargs) -> List[Structure]:
        data = self._cache.get_structures()
        res = list({
            'id': i[0],
            'shortName': i[1],
            'fullName': i[2]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_structures(*req_args, **req_kwargs)
            else: res = []
        return Structure.from_json(res)

    def list_faculties(self, structureId: int, *req_args, **req_kwargs) -> List[Faculty]:
        data = self._cache.get_faculties(structureId)
        res = list({
            'id': i[1],
            'shortName': i[2],
            'fullName': i[3]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_faculties(structureId, *req_args, **req_kwargs)
            else: res = []
        return Faculty.from_json(res)

    def list_courses(self, facultyId: int, *req_args, **req_kwargs) -> List[Course]:
        data = self._cache.get_courses(facultyId)
        res = list({
            'course': i[1]
        } for i in data)
        if len(res) == 0:
            if self.__http_enabled:
                res = super().list_courses(facultyId, *req_args, **req_kwargs)
            else: res = []
        return Course.from_json(res)

    def list_groups(self, facultyId: int, course: int, *req_args, **req_kwargs) -> List[Group]:
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
                res = super().list_groups(facultyId, course, *req_args, **req_kwargs)
            else: res = []
        return Group.from_json(res)
