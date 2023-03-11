# TODO: Change this module to telegram.ext.BasePersistence
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent


import os
import json
from functools import cache
from abc import ABC, abstractmethod
from .settings import langs, USER_DATA_PATH, CHAT_DATA_PATH

class DataManager(ABC):
    __data_cache = {}

    @property
    @abstractmethod
    def _DEFAULT_DATA(self) -> dict[str, any]:
        pass

    @classmethod
    def _get_data(cls, file: str) -> dict[str, any]:
        if file in cls.__data_cache:
            return cls.__data_cache[file]
        if not os.path.exists(file):
            fp = open(file, 'w')
            json.dump(cls._DEFAULT_DATA, fp, indent=4, ensure_ascii=False)
            fp.close()
            cls.__data_cache[file] = cls._DEFAULT_DATA.copy()
            return cls.__data_cache[file]
        cls.__data_cache[file] = json.load(open(file))
        return cls.__data_cache[file]

    @classmethod
    def _update_data(cls, file: str):
        fp = open(file, 'w')
        json.dump(cls._get_data(file), fp, indent=4, ensure_ascii=False)
        fp.close()

class UserData(DataManager):
    _DEFAULT_DATA = {
        'admin': False,
        'ref': None
    }

    def __init__(self, user_id: int | str) -> None:
        self._user_id = str(user_id)

    @cache
    def __get_file(self) -> str:
        return os.path.join(USER_DATA_PATH, '%s.json' % self._user_id)

    @property
    def admin(self) -> bool:
        return self._get_data(self.__get_file())['admin']
    @admin.setter
    def admin(self, val):
        self._get_data(self.__get_file())['admin'] = val
        self._update_data(self.__get_file())

    @property
    def ref(self) -> str | None:
        return self._get_data(self.__get_file())['ref']
    @ref.setter
    def ref(self, val):
        self._get_data(self.__get_file())['ref'] = val
        self._update_data(self.__get_file())

class ChatData(DataManager):
    _DEFAULT_DATA = {
        'lang_code': os.getenv('DEFAULT_LANG'),
        'group_id': None
    }

    def __init__(self, chat_id: int | str) -> None:
        self._chat_id = str(chat_id)

    @cache
    def __get_file(self) -> str:
        return os.path.join(CHAT_DATA_PATH, '%s.json' % self._chat_id)

    @property
    def lang_code(self) -> str:
        return self._get_data(self.__get_file())['lang_code']
    @lang_code.setter
    def lang_code(self, val):
        if not val in langs:
            val = os.getenv('DEFAULT_LANG')
        self._get_data(self.__get_file())['lang_code'] = val
        self._update_data(self.__get_file())

    @property
    def group_id(self) -> int | None:
        return self._get_data(self.__get_file())['group_id']
    @group_id.setter
    def group_id(self, val):
        self._get_data(self.__get_file())['group_id'] = val
        self._update_data(self.__get_file())

    @property
    def lang(self) -> dict[str, str]:
        return langs[self.lang_code]
