# pylint: disable=too-many-public-methods,missing-function-docstring,
# pylint: disable=too-many-arguments,line-too-long,keyword-arg-before-vararg

"""
API module for mkr.org.ua

API docs can be found at https://mkr.org.ua/portal-api-docs.html
"""

import json
import sqlite3
import logging
from typing import List
from datetime import datetime, timedelta, date as _date
from urllib.parse import urljoin

import pytz
import requests
from requests_cache import CachedSession

from . import utils

logger = logging.getLogger(__name__)
logger.info('Initializing api module')


class Api:
    """API wrapper for mkr.org.ua"""

    VERSION = '1.6.1'
    DEFAULT_LANGUAGE = 'uk'

    def __init__(self, url: str, timeout: int = None) -> None:
        """Creates an instance of the API wrapper
        
        :param url: URL of the API (see https://mkr.org.ua/api/v2/university/list)
        :param timeout: Timeout for requests (in seconds)
        """
        logger.info('Creating Api instance with url %s', url)

        self.url = url
        self.timeout = timeout
        self.session = requests.Session()

    def _make_request(self, path: str, method: str = 'GET',
                      json: dict = None, *req_args, **req_kwargs) -> requests.Response:

        self.session.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
            'Accept-Language': req_kwargs.pop('language', self.DEFAULT_LANGUAGE),
        })

        res = self.session.request(
            method=method,
            url=urljoin(self.url, path),
            json=json,
            timeout=self.timeout,
            *req_args, **req_kwargs
        )

        res.raise_for_status()
        return res

    # /time-table
    def timetable_group(self, group_id: int, date_start: _date | str,
                        date_end: _date | str | None = None,
                        *req_args, **req_kwargs) -> List[dict]:
        """Returns the schedule for the group"""

        date_start, date_start_str = utils.convert_date(date_start)
        if date_end is None:
            date_end = date_start
            date_end_str = date_start_str
        else:
            date_end, date_end_str = utils.convert_date(date_end)

        schedule = self._make_request('/time-table/group', 'POST', json={
            'groupId': group_id,
            'dateStart': date_start_str,
            'dateEnd': date_end_str
        }, *req_args, **req_kwargs).json()

        return utils.fill_empty_dates(schedule, date_start, date_end)

    def timetable_student(self, student_id: int, date_start: _date | str,
                          date_end: _date | str | None = None,
                          *req_args, **req_kwargs) -> List[dict]:
        """Returns the schedule for the student"""

        if isinstance(date_start, _date):
            date_start = date_start.isoformat()
        if date_end is None:
            date_end = date_start
        elif isinstance(date_end, _date):
            date_end = date_end.isoformat()

        return self._make_request('/time-table/student', 'POST', json={
            'studentId': student_id,
            'dateStart': date_start,
            'dateEnd': date_end
        }, *req_args, **req_kwargs).json()

    def timetable_teacher(self, teacher_id: int, date_start: _date | str,
                          date_end: _date | str | None = None,
                          *req_args, **req_kwargs) -> List[dict]:
        """Returns the schedule for the teacher"""

        if isinstance(date_start, _date):
            date_start = date_start.isoformat()
        if date_end is None:
            date_end = date_start
        elif isinstance(date_end, _date):
            date_end = date_end.isoformat()

        return self._make_request('/time-table/teacher', 'POST', json={
            'teacherId': teacher_id,
            'dateStart': date_start,
            'dateEnd': date_end
        }, *req_args, **req_kwargs).json()

    def timetable_classroom(self, classroom_id: int, date_start: _date | str,
                            date_end: _date | str | None = None,
                            *req_args, **req_kwargs) -> List[dict]:
        """Returns audience schedule (when and what groups are in it)"""

        if isinstance(date_start, _date):
            date_start = date_start.isoformat()
        if date_end is None:
            date_end = date_start
        elif isinstance(date_end, _date):
            date_end = date_end.isoformat()

        return self._make_request('/time-table/classroom', 'POST', json={
            'classroomId': classroom_id,
            'dateStart': date_start.isoformat(),
            'dateEnd': date_end.isoformat()
        }, *req_args, **req_kwargs).json()

    def timetable_call_schedule(self, *req_args, **req_kwargs) -> List[dict]:
        """Returns the call schedule"""
        return self._make_request('/time-table/call-schedule', 'POST',
            *req_args, **req_kwargs).json()

    def timetable_ad(self, class_code: int, date: _date | str, *req_args, **req_kwargs) -> dict:
        """Returns an announcement for the current lesson\n
        Usually contains a lesson link in Teams/Zoom"""

        if isinstance(date, _date):
            date = date.isoformat()

        return self._make_request('/time-table/schedule-ad', 'POST', json={
            'r1': class_code,
            'r2': date
        }, *req_args, **req_kwargs).json()

    def timetable_free_classrooms(self, structure_id: int, corpus_id: int,
                                  lesson_number_start: int, lesson_number_end: int,
                                  date: datetime | str, *req_args, **req_kwargs) -> List[dict]:
        """Returns list of free classrooms
        Date format: `2023-02-23T10:26:00.000Z` or `datetime.datetime`"""

        if isinstance(date, datetime):
            date = date.astimezone(pytz.UTC).isoformat(sep='T', timespec='milliseconds') + 'Z'

        return self._make_request('/time-table/free-classroom', 'POST', json={
            'structureId': structure_id,
            'corpusId': corpus_id,
            'lessonNumberStart': lesson_number_start,
            'lessonNumberEnd': lesson_number_end,
            'date': date
        }, *req_args, **req_kwargs).json()

    # /list
    def list_structures(self, *req_args, **req_kwargs) -> List[dict]:
        """Returns list of structures"""
        return self._make_request('/list/structures', *req_args, **req_kwargs).json()

    def list_faculties(self, structure_id: int, *req_args, **req_kwargs) -> List[dict]:
        """Returns list of faculties"""
        return self._make_request('/list/faculties', 'POST', json={
            'structureId': structure_id
        }, *req_args, **req_kwargs).json()

    def list_courses(self, faculty_id: int, *req_args, **req_kwargs) -> List[dict]:
        """Returns list of courses"""
        return self._make_request('/list/courses', 'POST', json={
            'facultyId': faculty_id
        }, *req_args, **req_kwargs).json()

    def list_groups(self, faculty_id: int, course: int, *req_args, **req_kwargs) -> List[dict]:
        """Return list of groups"""
        return self._make_request('/list/groups', 'POST', json={
            'facultyId': faculty_id,
            'course': course
        }, *req_args, **req_kwargs).json()

    def list_chairs(self, structure_id: int, faculty_id: int,
                    *req_args, **req_kwargs) -> List[dict]:
        """Returns list of chairs"""
        return self._make_request('/list/chairs', 'POST', json={
            'structureId': structure_id,
            'facultyId': faculty_id
        }, *req_args, **req_kwargs).json()

    def list_teachers_by_chair(self, chair_id: int, *req_args, **req_kwargs) -> List[dict]:
        """Returns a list of teachers from the given chair"""
        return self._make_request('/list/teachers-by-chair', 'POST', json={
            'chairId': chair_id
        }, *req_args, **req_kwargs).json()

    def list_students_by_group(self, group_id: int, *req_args, **req_kwargs) -> List[dict]:
        """Returns a list of students from the given group"""
        return self._make_request('/list/students-by-group', 'POST', json={
            'groupId': group_id
        }, *req_args, **req_kwargs).json()

    # /other
    def search_teacher(self, name: str, *req_args, **req_kwargs) -> List[dict]:
        """Looking for a teacher by a fragment of his last name only\n
        Not case sensitive, returns an array of the first 50 teachers found"""
        return self._make_request('/other/search-teachers', 'POST', json={
            'name': name
        }, *req_args, **req_kwargs).json()

    # General
    def icon(self, *req_args, **req_kwargs) -> bytes:
        """Returns the university logo"""
        return self._make_request('/icon', *req_args, **req_kwargs).content

    def version(self, *req_args, **req_kwargs) -> dict:
        """Returns the version of the API"""
        return self._make_request('/version', *req_args, **req_kwargs).json()

    # Not implemented
    def timetable_universal(self, date: _date | str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def user_info2(self, id_: int, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def user_info(self, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def user_change_password(self, password: str, new_password: str,
                             *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def user_change_password2(self, id_: int, new_password: str,
                              *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def user_delete(self, id_: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def user_update2(self, id_: int, blocked: int, username: str,
                     email: str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def user_update(self, username: str, email: str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def user_create(self, id_: int, type_: int, username: str,
                    email: str, password: str, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def user_search_student(self, code: int, birthday: _date | str,
                            type_: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def user_search_teacher(self, inn: str, birthday: _date | str,
                            *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def user_change_account(self, type_: int, id_: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def user_change_account2(self, id_: int, type_: int, new_id: int,
                             *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def inquiry_types(self, faculty_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def journal_student(self, year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def journal_full_discipline_journal(self, discipline_id: int, type_: int, year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def student_semester_list(self, only_active: bool, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def student_info(self, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def student_search_by_email(self, email: str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def student_search(self, last_name: str, faculty_id: int, speciality_full_name: str, course: int, group_name: str, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def docs_get_new_docs(self, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def docs_mark_docs_as_read(self, docs: List[int], *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def docs_get_docs_on_control(self, count_days: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_dols(self, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_structures(self, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_faculties(self, structure_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_chairs(self, structure_id: int, faculty_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_teacher_identifiers(self, last_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_chair_info(self, chair_ids: List[int], *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_group_info(self, group_ids: List[int], *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_students(self, last_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_teachers(self, last_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def org_set_external_ids(self, external_ids: List[dict], *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def login(self, username: str, password: str, app_key: str, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def auth_data(self, username: str, password: str, key: str, *req_args, **req_kwargs) -> dict:
        raise NotImplementedError

    def academ_disciplines(self, last_id: int, year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def academ_learning_plans(self, discipline_ids: List[int], year: int, semester: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def exam_sheets(self, year: int, semester: int, education_discipline_id: int, group_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def exam_statement_list(self, year: int, semester: int, education_discipline_id: int, group_id: int, *req_args, **req_kwargs) -> List[dict]:
        raise NotImplementedError

    def exam_set_date_enter(self, sheet_id: int, date_enter: _date | str, *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def exam_close(self, sheet_id: int, *req_args, **req_kwargs) -> None:
        raise NotImplementedError

    def exam_set_marks(self, sheet_id: int, marks: List[dict], *req_args, **req_kwargs) -> None:
        raise NotImplementedError


class CachedApi(Api):
    """API wrapper for mkr.org.ua with caching enabled"""

    SCHEDULE_CACHE_DAYS_RANGE = 14

    def __init__(
            self, url: str, timeout: int = None, cache_path: str = 'api-cache.sqlite',
            cache_expires: int | timedelta | None = None, **cache_kwargs):
        """Creates an instance of the API wrapper with caching enabled
        
        :param url: URL of the API (see https://mkr.org.ua/api/v2/university/list)
        :param timeout: Timeout for requests (in seconds)
        :param cache_path: Path to the cache database
        :param cache_expires: Cache expiration time (in seconds or timedelta)
        :param cache_kwargs: Additional kwargs for requests_cache.CachedSession
        """
        super().__init__(url=url, timeout=timeout)

        if cache_expires is None:
            self.cache_expires = None
        elif isinstance(cache_expires, timedelta):
            if cache_expires.total_seconds() <= 0:
                self.cache_expires = None
            else:
                self.cache_expires = cache_expires
        elif isinstance(cache_expires, int):
            if cache_expires <= 0:
                self.cache_expires = None
            else:
                self.cache_expires = timedelta(seconds=cache_expires)
        else:
            raise TypeError('cache_expires must be int, timedelta or None')

        self.session = CachedSession(
            cache_control=True,
            allowable_methods=['GET', 'POST'],
            match_headers=True,
            stale_if_error=True,
            expire_after=cache_expires,
            **cache_kwargs
        )

        self.cache_path = cache_path
        self._conn = sqlite3.connect(cache_path)
        self._cursor = self._conn.cursor()
        utils.setup_db(self._conn)

    def timetable_group(
            self, group_id: int, date_start: _date | str,
            date_end: _date | str | None = None,
            *req_args, **req_kwargs) -> List['CachedResult']:
        """Returns the schedule for the group"""

        if isinstance(date_start, _date):
            date_start_str = date_start.isoformat()
        else:
            date_start_str = date_start
            date_start = _date.fromisoformat(date_start)

        if date_end is None:
            date_end = date_start
            date_end_str = date_start_str
        elif isinstance(date_end, _date):
            date_end_str = date_end.isoformat()
        else:
            date_end_str = date_end
            date_end = _date.fromisoformat(date_end)

        cached = self._cursor.execute(
            'SELECT * FROM group_schedule WHERE group_id = ? AND date BETWEEN ? AND ? AND language = ?',
            (group_id, date_start_str, date_end_str, req_kwargs.get('language', self.DEFAULT_LANGUAGE))
        ).fetchall()

        # Check if we need to update cache
        if len(cached) < (date_end - date_start).days + 1:
            # If we are missing some dates in cache, we need to update it
            cache_update_needed = True
        elif self.cache_expires is not None:
            # Check if we need to update some dates in cache
            cur_time = datetime.now()
            for row in cached:
                if (cur_time - datetime.fromisoformat(row[4])) >= self.cache_expires:
                    cache_update_needed = True
                    break
            else:
                cache_update_needed = False
        else:
            cache_update_needed = False

        if cache_update_needed:
            logger.debug('Updating cache for group %s for %s to %s', group_id, date_start_str, date_end_str)

            # Get dates range
            date_range_start, date_range_end = utils.get_date_range(date_start, self.SCHEDULE_CACHE_DAYS_RANGE)
            if date_end_str != date_start_str:
                _, date_range_end = utils.get_date_range(date_end, self.SCHEDULE_CACHE_DAYS_RANGE)

            schedule = super().timetable_group(
                group_id=group_id,
                date_start=date_range_start,
                date_end=date_range_end,
                *req_args, **req_kwargs
            )

            # Update cache
            updated_time = datetime.now().isoformat(sep=' ', timespec='seconds')
            for day in schedule:
                self._cursor.execute(
                    'INSERT OR REPLACE INTO group_schedule VALUES (?, ?, ?, ?, ?)', (
                        group_id,
                        day['date'],
                        req_kwargs.get('language', self.DEFAULT_LANGUAGE),
                        json.dumps(day['lessons'], ensure_ascii=False),
                        updated_time
                    )
                )
            self._conn.commit()

            # Return only needed dates
            result = []
            for day in schedule:
                if date_start <= _date.fromisoformat(day['date']) <= date_end:
                    result.append(CachedResult(
                        data=day,
                        updated=datetime.fromisoformat(updated_time),
                        expires_in=self.cache_expires
                    ))
            return result
        
        # Convert cached data to needed format and return it
        result = []
        for row in cached:
            result.append(CachedResult(
            data={
                'date': row[1],
                'lessons': json.loads(row[3])
            },
            updated=datetime.fromisoformat(row[4]),
            expires_in=self.cache_expires))

        return result


class CachedResult(dict):
    """Dict wrapper for cached result of the API request"""

    def __init__(self, data: dict, updated: datetime, expires_in: timedelta):
        super().__init__(data)
        self.updated = updated
        self.expires_in = expires_in

    @property
    def expires(self) -> datetime:
        return self.updated + self.expires_in

    @property
    def expired(self) -> bool:
        return datetime.now() >= self.expires
