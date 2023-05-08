# TODO: Change this module to telegram.ext.BasePersistence
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent


import os
import time
import json
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from functools import cache
from dataclasses import dataclass, field as _field
from settings import langs, USER_DATA_PATH, CHAT_DATA_PATH


@dataclass(frozen=True)
class Message:
    id: int
    timestamp: datetime
    page_name: str
    lang_code: str
    data: dict[str, any] = _field(default_factory=dict)


class DataManager(ABC):
    @staticmethod
    @abstractmethod
    def _get_default_data() -> dict[str, any]:
        pass

    _data_cache: dict[str, dict[str, any]] = {}

    @classmethod
    def _get_data(cls, file: str) -> dict[str, any]:
        data = cls._data_cache.get(file)
        if data:
            return data
        if not os.path.exists(file):
            data = cls._get_default_data()
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
    @staticmethod
    def _get_default_data() -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'admin': False,
            'ref': None,
            '_created': cur_timestamp_s,
            '_updated': cur_timestamp_s
        }

    @staticmethod
    def get_all():
        for file in os.listdir(USER_DATA_PATH):
            yield ChatData(Path(file).stem)

    @staticmethod
    def exists(chat_id: int | str) -> bool:
        for file in os.listdir(CHAT_DATA_PATH):
            _chat_id = Path(file).stem
            if _chat_id == str(chat_id):
                return True
        return False

    def __init__(self, user_id: int | str) -> None:
        self._user_id = str(user_id)

    @cache
    def _get_file(self) -> str:
        return os.path.join(USER_DATA_PATH, '%s.json' % self._user_id)

    def get(self, name: str) -> any:
        return self._get_data(self._get_file())[name]

    def set(self, name: str, value: any):
        data = self._get_data(self._get_file())
        data[name] = value
        self._update_data(self._get_file())


class ChatData(DataManager):
    @staticmethod
    def _get_default_data() -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'lang_code': os.getenv('DEFAULT_LANG'),  # Language code
            'group_id': None,  # Group ID
            'cl_notif_15m': False,  # Notification 15 minutes before class
            'cl_notif_1m': False,  # Notification when classes starts
            'cl_notif_suggested': False,  # Is classes notification suggested
            '_messages': [],  # List of bot messages sent to chat
            '_accessible': True,  # No access to chat (user blocked bot or no access to chat)
            '_created': cur_timestamp_s,  # Chat creation timestamp
            '_updated': cur_timestamp_s  # Chat latest update timestamp
        }

    MESSAGES_LIMIT = 16

    @staticmethod
    def get_all():
        for file in os.listdir(CHAT_DATA_PATH):
            yield ChatData(Path(file).stem)

    @staticmethod
    def exists(chat_id: int | str) -> bool:
        for file in os.listdir(CHAT_DATA_PATH):
            _chat_id = Path(file).stem
            if _chat_id == str(chat_id):
                return True
        return False

    def __init__(self, chat_id: int | str) -> None:
        self._chat_id = str(chat_id)

    @cache
    def __get_file(self) -> str:
        return os.path.join(CHAT_DATA_PATH, '%s.json' % self._chat_id)

    def get(self, field: str) -> any:
        return self._get_data(self.__get_file())[field]

    def set(self, field: str, value: any):
        data = self._get_data(self.__get_file())
        data[field] = value
        self._update_data(self.__get_file())

    def get_lang(self) -> dict[str, str]:
        return langs[self.get('lang_code')]

    def get_messages(self, page_name: str = None) -> list[Message]:
        messages = self.get('_messages')
        res = []
        for m in messages:
            if page_name is not None and m[2] != page_name:
                continue
            res.append(Message(m[0], datetime.fromtimestamp(m[1]), m[2], m[3], m[4]))
        return res

    def add_message(self, msg: Message):
        messages_raw = self.get('_messages')
        msg_raw = [msg.id, int(msg.timestamp.timestamp()), msg.page_name, msg.lang_code, msg.data]

        # Add a message or update an old one with this ID
        for i, m in enumerate(messages_raw):
            if m[0] == msg.id:
                messages_raw[i] = msg_raw
                break
        else:
            messages_raw.append(msg_raw)

        if len(messages_raw) > self.MESSAGES_LIMIT:
            messages_raw.pop(0)

        self._update_data(self.__get_file())

    def remove_message(self, msg_id: int):
        messages_raw = self.get('_messages')
        for i, m in enumerate(messages_raw):
            if m[0] == msg_id:
                messages_raw.pop(i)
                break
        self._update_data(self.__get_file())
