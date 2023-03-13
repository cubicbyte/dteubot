# TODO: Change this module to telegram.ext.BasePersistence
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent


import os
import time
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
    def _get_data(cls, file: str, ignore_cache: bool = False) -> dict[str, any]:
        if not ignore_cache and file in cls.__data_cache:
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
    @property
    def _DEFAULT_DATA(self) -> dict[str, any]:
        return {
            'admin': False,
            'ref': None
        }

    def __init__(self, user_id: int | str) -> None:
        self._user_id = str(user_id)

    @cache
    def __get_file(self) -> str:
        return os.path.join(USER_DATA_PATH, '%s.json' % self._user_id)

    def __getattr__(self, __name: str) -> any:
        return self._get_data(self.__get_file())[__name]

    def __setattr__(self, __name: str, __value: any):
        self._get_data(self.__get_file())[__name] = __value
        self._update_data(self.__get_file())

class ChatData(DataManager):
    @property
    def _DEFAULT_DATA(self) -> dict[str, any]:
        return {
            'lang_code': os.getenv('DEFAULT_LANG'),
            'group_id': None
        }

    def __init__(self, chat_id: int | str) -> None:
        self._chat_id = str(chat_id)

    @cache
    def __get_file(self) -> str:
        return os.path.join(CHAT_DATA_PATH, '%s.json' % self._chat_id)

    def __getattr__(self, __name: str) -> any:
        return self._get_data(self.__get_file())[__name]

    def __setattr__(self, __name: str, __value: any):
        self._get_data(self.__get_file())[__name] = __value
        self._update_data(self.__get_file())

    @property
    def lang_code(self) -> str:
        return self.__getattr__('lang_code')
    @property
    def lang_code(self, val):
        if not val in langs:
            val = os.getenv('DEFAULT_LANG')
        self.__setattr__('lang_code', val)

    def get_lang(self) -> dict[str, str]:
        return langs[self.lang_code]
