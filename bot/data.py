"""
Data management module.
"""

import os
import time
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime

from telegram import Update, Message as TgMessage
from telegram.ext import ContextTypes

from settings import langs
from bot.schemas import StoredMessage, Language

logger = logging.getLogger(__name__)


class ContextManager:
    # pylint: disable=too-few-public-methods
    """
    Context manager for bot commands and callbacks.
    Provides access to user and chat data.
    """

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.update = update
        self.context = context
        self.chat_data = ChatData(update.effective_chat.id)
        self.user_data = UserData(update.effective_user.id)

    @property
    def lang(self) -> Language:
        """Get chat language"""
        return self.chat_data.lang


class DataManager(ABC):
    """Abstract data manager class"""

    @staticmethod
    @abstractmethod
    def _get_default_data() -> dict[str, any]:
        pass

    @abstractmethod
    def _get_file(self) -> str:
        pass

    _data_cache: dict[str, dict[str, any]] = {}

    @classmethod
    def _get_data(cls, filepath: str) -> dict[str, any]:
        """Load data from file or cache"""

        # If data is in cache, return it
        data = cls._data_cache.get(filepath)
        if data:
            return data

        # If file doesn't exist, create it and return default data
        if not os.path.exists(filepath):
            data = cls._get_default_data()
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            cls._data_cache[filepath] = data
            return cls._data_cache[filepath]

        # Load data from file and return it
        with open(filepath, encoding='utf-8') as file:
            data = json.load(file)
        cls._data_cache[filepath] = data
        return data

    @classmethod
    def _update_data(cls, filepath: str, no_update: bool = False):
        """Flush data from cache to file"""

        data = cls._data_cache.get(filepath) or cls._get_default_data()

        # Set latest data update timestamp
        if not no_update:
            data['_updated'] = int(time.time())

        # Save data to file
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

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
        self.user_id = int(user_id)

    def _get_file(self) -> str:
        """Get user data file path"""
        return os.path.join(os.getenv('USER_DATA_PATH'), f'{self.user_id}.json')

    @staticmethod
    def _get_default_data() -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'admin': False,
            'ref': None,
            '_created': cur_timestamp_s,
            '_updated': cur_timestamp_s,
        }
        # Fields description:
        # admin: is user admin
        # ref: referral code (to know where user came from)
        # _created: user data creation timestamp
        # _updated: user data latest update timestamp

    @staticmethod
    def get_all():
        """Iterate over all user data"""
        for file in os.listdir(os.getenv('USER_DATA_PATH')):
            yield ChatData(Path(file).stem)

    @staticmethod
    def exists(chat_id: int | str) -> bool:
        """Check if user data exists"""
        filepath = os.path.join(os.getenv('USER_DATA_PATH'), f'{chat_id}.json')
        return os.path.exists(filepath)


class ChatData(DataManager):
    """Chat data manager"""

    MESSAGES_LIMIT = 16
    "Saved messages limit"

    def __init__(self, chat_id: int | str) -> None:
        self.chat_id = int(chat_id)

    @staticmethod
    def _get_default_data() -> dict[str, any]:
        cur_timestamp_s = int(time.time())
        return {
            'lang_code': os.getenv('DEFAULT_LANG'),
            'group_id': None,
            'cl_notif_15m': False,
            'cl_notif_1m': False,
            'seen_settings': False,
            '_messages': [],
            '_accessible': True,
            '_created': cur_timestamp_s,
            '_updated': cur_timestamp_s,
        }
        # Fields description:
        # lang_code: chat language
        # group_id: group id to get schedule from
        # cl_notif_15m: is 15 minutes before class notification enabled
        # cl_notif_1m: is 1 minute before class notification enabled
        # seen_settings: is user opened settings menu.
        #                If not, after some time bot will suggest classes notification
        # _messages: list of bot messages sent to chat
        # _accessible: is chat accessible (like user blocked bot)
        # _created: chat data creation timestamp
        # _updated: chat data latest update timestamp

    @staticmethod
    def get_all():
        """Iterate over all chat data"""
        for file in os.listdir(os.getenv('CHAT_DATA_PATH')):
            yield ChatData(Path(file).stem)

    @staticmethod
    def exists(chat_id: int | str) -> bool:
        """Check if chat data exists"""
        filepath = os.path.join(os.getenv('CHAT_DATA_PATH'), f'{chat_id}.json')
        return os.path.exists(filepath)

    def _get_file(self) -> str:
        """Get chat data file path"""
        return os.path.join(os.getenv('CHAT_DATA_PATH'), f'{self.chat_id}.json')

    @property
    def lang(self) -> Language:
        """Get chat language object"""
        return langs.get(self.get('lang_code')) or \
               langs.get(os.getenv('DEFAULT_LANG'))

    def get_messages(self, page_name: str = None) -> list[StoredMessage]:
        """Get all saved messages from database"""

        messages_raw = self.get('_messages')
        messages = []

        for msg in messages_raw:
            # Filter messages by page name
            if page_name is not None and msg[2] != page_name:
                continue

            messages.append(StoredMessage(msg[0], datetime.fromtimestamp(msg[1]),
                            msg[2], msg[3], msg[4]))

        return messages

    def add_message(self, message: StoredMessage):
        """Save a message to database"""

        messages_raw = self.get('_messages')
        message_raw = [message.id, int(message.timestamp.timestamp()),
                       message.page_name, message.lang_code, message.data]

        # Update message if it exists
        for i, msg in enumerate(messages_raw):
            if msg[0] == message.id:
                messages_raw[i] = message_raw
                break
        # Add message if it doesn't exist
        else:
            messages_raw.append(message_raw)

        # Limit messages count
        if len(messages_raw) > self.MESSAGES_LIMIT:
            messages_raw.pop(0)

        self.set('_messages', messages_raw)

    def save_message(
            self,
            page_name: str,
            message: TgMessage,
            data: dict | None = None
    ):
        """Fast shortcut for `add_message`"""

        self.add_message(StoredMessage(
            message.message_id,
            message.date,
            page_name,
            self.get('lang_code'),
            data,
        ))

    def remove_message(self, msg_id: int):
        """Remove saved message from database"""

        messages_raw = self.get('_messages')

        for i, msg in enumerate(messages_raw):
            if msg[0] == msg_id:
                messages_raw.pop(i)
                break

        self._update_data(self._get_file())
