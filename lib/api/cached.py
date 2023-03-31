import os
import json
from datetime import date as _date, timedelta
from requests_cache import DEFAULT_CACHE_NAME
from . import Api
from .schemas import *
from ..cache_reader import CacheReader

class CachedApi(Api):
    def __init__(self, url: str, *api_args, enable_http: bool = False, **api_kwargs):
        super().__init__(url, *api_args, **api_kwargs)
        cache_name = DEFAULT_CACHE_NAME if not 'cache_name' in api_kwargs else api_kwargs['cache_name']
        cache_path = os.path.join(os.path.dirname(cache_name), 'mkr-cache.sqlite')
        self._http_enabled = enable_http
        self._cache = CacheReader(cache_path)

    def timetable_group(self, groupId: int, dateStart: _date, dateEnd: _date = None, *req_args, **req_kwargs) -> List[TimeTableDate]:
        if dateEnd is None:
            dateEnd = dateStart
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
