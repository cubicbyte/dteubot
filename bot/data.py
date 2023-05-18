# TODO: Change this module to telegram.ext.BasePersistence
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent


import os
import time
import json
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
from datetime import datetime
from functools import cache
from dataclasses import dataclass, field as _field
from telegram import Message as TgMessage
from settings import langs


@dataclass(frozen=True)
class Message:
    id: int
    timestamp: datetime
    page_name: str
    lang_code: str
    data: dict[str, any] = _field(default_factory=dict)

    @classmethod
    def create(cls, name: str, message: TgMessage):
        return cls(
            message.message_id,
            message.date,
            name,
            message.from_user.language_code
        )


class DataManager(ABC):
    @staticmethod
    @abstractmethod
    def _get_default_data() -> dict[str, any]:
        pass

    @abstractmethod
    def _get_file(self) -> str:
        pass

    _data_cache: dict[str, dict[str, any]] = {}

    @classmethod
    def _get_data(cls, file: str) -> dict[str, any]:
        """Load data from file or cache"""

        # If data is in cache, return it
        data = cls._data_cache.get(file)
        if data:
            return data

        # If file doesn't exist, create it and return default data
        if not os.path.exists(file):
            data = cls._get_default_data()
            with open(file, 'w') as fp:
                json.dump(data, fp, indent=4, ensure_ascii=False)
            cls._data_cache[file] = data
            return cls._data_cache[file]

        # Load data from file and return it
        with open(file) as fp:
            data = json.load(fp)
        cls._data_cache[file] = data
        return data

    @classmethod
    def _update_data(cls, file: str, no_update: bool = False):
        """Flush data from cache to file"""

        data = cls._data_cache.get(file) or cls._get_default_data()

        # Set latest data update timestamp
        if not no_update:
            data['_updated'] = int(time.time())

        # Save data to file
        with open(file, 'w') as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)

    def get(self, field: str) -> any:
        """Get chat data field"""
        return self._get_data(self._get_file())[field]

    def set(self, field: str, value: any, no_update: bool = False):
        """Set chat data field"""

        data = self._get_data(self._get_file())
        data[field] = value
        self._update_data(self._get_file(), no_update=no_update)


class UserData(DataManager):
    """User data manager"""

    def __init__(self, user_id: int | str) -> None:
        self._user_id = str(user_id)

    @cache
    def _get_file(self) -> str:
        """Get user data file path"""
        return os.path.join(os.getenv('USER_DATA_PATH'), '%s.json' % self._user_id)

    @staticmethod
    def _get_default_data() -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'admin': False,               # Is user admin
            'ref': None,                  # Referral code
            '_created': cur_timestamp_s,  # User data creation timestamp
            '_updated': cur_timestamp_s,  # User data last update timestamp
        }

    @staticmethod
    def get_all():
        """Iterate over all user data"""
        for file in os.listdir(os.getenv('USER_DATA_PATH')):
            yield ChatData(Path(file).stem)

    @staticmethod
    def exists(chat_id: int | str) -> bool:
        """Check if user data exists"""
        filepath = os.path.join(os.getenv('USER_DATA_PATH'), '%s.json' % chat_id)
        return os.path.exists(filepath)


class ChatData(DataManager):
    """Chat data manager"""

    MESSAGES_LIMIT = 16
    "Saved messages limit"

    def __init__(self, chat_id: int | str) -> None:
        self._chat_id = str(chat_id)

    @staticmethod
    def _get_default_data() -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'lang_code': os.getenv('DEFAULT_LANG'),
            'group_id': None,
            'cl_notif_15m': False,        # Notification 15 minutes before class
            'cl_notif_1m': False,         # Notification when classes starts
            'cl_notif_suggested': False,  # Is classes notification suggested
            '_messages': [],              # List of bot messages sent to chat
            '_accessible': True,          # Is chat accessible (user blocked bot or no access to chat)
            '_created': cur_timestamp_s,  # Chat creation timestamp
            '_updated': cur_timestamp_s,  # Chat latest update timestamp
        }

    @staticmethod
    def get_all():
        """Iterate over all chat data"""
        for file in os.listdir(os.getenv('CHAT_DATA_PATH')):
            yield ChatData(Path(file).stem)

    @staticmethod
    def exists(chat_id: int | str) -> bool:
        """Check if chat data exists"""
        filepath = os.path.join(os.getenv('CHAT_DATA_PATH'), '%s.json' % chat_id)
        return os.path.exists(filepath)

    @cache
    def _get_file(self) -> str:
        """Get chat data file path"""
        return os.path.join(os.getenv('CHAT_DATA_PATH'), '%s.json' % self._chat_id)

    def get_lang(self) -> dict[str, str]:
        """Get chat language"""
        return langs.get(self.get('lang_code')) or \
               langs.get(os.getenv('DEFAULT_LANG'))

    def get_messages(self, page_name: str = None) -> list[Message]:
        """Get all saved messages from database"""

        messages_raw = self.get('_messages')
        messages = []
 
        for msg in messages_raw:
            # Filter messages by page name
            if page_name is not None and msg[2] != page_name:
                continue

            messages.append(Message(msg[0], datetime.fromtimestamp(msg[1]),
                            msg[2], msg[3], msg[4]))

        return messages

    def add_message(self, msg: Message):
        """Save a message to database"""

        messages_raw = self.get('_messages')
        message_raw = [msg.id, int(msg.timestamp.timestamp()),
                       msg.page_name, msg.lang_code, msg.data]

        # Update message if it exists
        for i, m in enumerate(messages_raw):
            if m[0] == msg.id:
                messages_raw[i] = message_raw
                break
        # Add message if it doesn't exist
        else:
            messages_raw.append(message_raw)

        # Limit messages count
        if len(messages_raw) > self.MESSAGES_LIMIT:
            messages_raw.pop(0)

        self._update_data(self._get_file())

    def save_message(
            self,
            page_name: str,
            message: TgMessage,
            data: Optional[dict] = None
    ):
        """Fast shortcut for `add_message`"""

        self.add_message(Message(
            message.message_id,
            message.date,
            page_name,
            self.get('lang_code'),
            data,
        ))

    def remove_message(self, msg_id: int):
        """Remove saved message from database"""

        messages_raw = self.get('_messages')

        for i, m in enumerate(messages_raw):
            if m[0] == msg_id:
                messages_raw.pop(i)
                break

        self._update_data(self._get_file())
