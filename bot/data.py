# TODO: Change this module to telegram.ext.BasePersistence
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent


import os
import time
import json
from functools import cache
from abc import ABC, abstractmethod
from .settings import langs, USER_DATA_PATH, CHAT_DATA_PATH

class DataManager(ABC):
    _data_cache: dict[str, dict[str, any]] = {}

    @property
    @abstractmethod
    def _DEFAULT_DATA(self) -> dict[str, any]:
        pass

    @classmethod
    def _get_data(cls, file: str) -> dict[str, any]:
        data = cls._data_cache.get(file)
        if data:
            return data
        if not os.path.exists(file):
            data = cls._DEFAULT_DATA.copy()
            with open(file, 'w') as fp:
                json.dump(data, fp, indent=4, ensure_ascii=False)
            cls._data_cache[file] = data
            return cls._data_cache[file]
        with open(file) as fp:
            data = json.load(fp)
        cls._data_cache[file] = data
        return data

    @classmethod
    def _update_data(cls, file: str):
        with open(file, 'w') as fp:
            json.dump(cls._get_data(file), fp, indent=4, ensure_ascii=False)

class UserData(DataManager):
    @property
    def _DEFAULT_DATA(self) -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'admin': False,
            'ref': None,
            '_created': cur_timestamp_s,
            '_updated': cur_timestamp_s
        }

    def __init__(self, user_id: int | str) -> None:
        self._user_id = str(user_id)

    @cache
    def _get_file(self) -> str:
        return os.path.join(USER_DATA_PATH, '%s.json' % self._user_id)

    def __getattr(self, name: str) -> any:
        return self._get_data(self._get_file())[name]

    def __setattr(self, name: str, value: any):
        data = self._get_data(self._get_file())
        data[name] = value
        if not name.startswith('_'):
            data['_updated'] = int(time.time())
        self._update_data(self._get_file())

    @property
    def admin(self) -> bool:
        return self.__getattr('admin')
    @property
    def ref(self) -> str | None:
        return self.__getattr('ref')
    @property
    def _created(self) -> int:
        return self.__getattr('_created')
    @property
    def _updated(self) -> int:
        return self.__getattr('_updated')

    @admin.setter
    def admin(self, value: bool):
        self.__setattr('admin', value)
    @ref.setter
    def ref(self, value: str | None):
        self.__setattr('ref', value)
    @_created.setter
    def _created(self, value: int):
        self.__setattr('_created', value)
    @_updated.setter
    def _updated(self, value: int):
        self.__setattr('_updated', value)

class ChatData(DataManager):
    @property
    def _DEFAULT_DATA(self) -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'lang_code': os.getenv('DEFAULT_LANG'), # Language code
            'group_id': None,                       # Group ID
            'cl_notif_15m': False,                  # Notification 15 minutes before class
            'cl_notif_1m': False,                   # Notification when classes starts
            '_accessible': True,                    # No access to chat (user blocked bot or no access to chat)
            '_created': cur_timestamp_s,            # Chat creation timestamp
            '_updated': cur_timestamp_s             # Chat latest update timestamp
        }

    def __init__(self, chat_id: int | str) -> None:
        self._chat_id = str(chat_id)

    @cache
    def __get_file(self) -> str:
        return os.path.join(CHAT_DATA_PATH, '%s.json' % self._chat_id)

    def __getattr(self, name: str) -> any:
        return self._get_data(self.__get_file())[name]

    def __setattr(self, name: str, value: any):
        data = self._get_data(self.__get_file())
        data[name] = value
        if not name.startswith('_'):
            data['_updated'] = int(time.time())
        self._update_data(self.__get_file())

    def get_lang(self) -> dict[str, str]:
        return langs[self.lang_code]

    @property
    def lang_code(self) -> str:
        return self.__getattr('lang_code')
    @property
    def group_id(self) -> str | None:
        return self.__getattr('group_id')
    @property
    def cl_notif_15m(self) -> bool:
        return self.__getattr('cl_notif_15m')
    @property
    def cl_notif_1m(self) -> bool:
        return self.__getattr('cl_notif_1m')
    @property
    def cl_notif_suggested(self) -> bool:
        return self.__getattr('cl_notif_suggested')
    @property
    def _accessible(self) -> bool:
        return self.__getattr('_accessible')
    @property
    def _created(self) -> int:
        return self.__getattr('_created')
    @property
    def _updated(self) -> int:
        return self.__getattr('_updated')

    @lang_code.setter
    def lang_code(self, value: str):
        if not value in langs:
            value = os.getenv('DEFAULT_LANG')
        self.__setattr('lang_code', value)
    @group_id.setter
    def group_id(self, value: str | None):
        self.__setattr('group_id', value)
    @cl_notif_15m.setter
    def cl_notif_15m(self, value: bool):
        self.__setattr('cl_notif_15m', value)
    @cl_notif_1m.setter
    def cl_notif_1m(self, value: bool):
        self.__setattr('cl_notif_1m', value)
    @cl_notif_suggested.setter
    def cl_notif_suggested(self, value: bool):
        self.__setattr('cl_notif_suggested', value)
    @_accessible.setter
    def _accessible(self, value: bool):
        self.__setattr('_accessible', value)
    @_created.setter
    def _created(self, value: int):
        self.__setattr('_created', value)
    @_updated.setter
    def _updated(self, value: int):
        self.__setattr('_updated', value)
