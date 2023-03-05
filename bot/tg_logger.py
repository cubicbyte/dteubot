import os
import logging
import json
from datetime import datetime
from pathlib import Path
from telebot import types, TeleBot
from .utils.fs import mkdir, mkdir_safe, create_file, open_file


logger = logging.getLogger(__name__)



class TelegramLogger:
    """Logger to log messages/button clicks"""
    def __init__(self, dirpath):
        logger.debug('Creating TelegramLogger instance')

        self.__dirpath = dirpath
        self.__init_dirs()

    def get_chat_log_dir(self, chat_id: int) -> Path:
        """Returns chat log dirpath"""
        return Path(self.__dirpath, 'chats', str(chat_id))

    def get_user_log_dir(self, user_id: int) -> Path:
        """Returns user log dirpath"""
        return Path(self.__dirpath, 'users', str(user_id))

    def __init_dirs(self):
        logger.info('Initializing TelegramLogger dirs')
        mkdir_safe(self.__dirpath)
        mkdir_safe(Path(self.__dirpath, 'chats'))
        mkdir_safe(Path(self.__dirpath, 'users'))

    def __chat_log_initialized(self, chat_id: int) -> bool:
        return os.path.exists(self.get_chat_log_dir(chat_id))

    def __user_log_initialized(self, user_id: int) -> bool:
        return os.path.exists(self.get_user_log_dir(user_id))

    def __init_chat_log(self, chat_id: int):
        logger.info('Initializing %s chat log' % chat_id)
        dirpath = self.get_chat_log_dir(chat_id)
        mkdir(dirpath)
        create_file(Path(dirpath, 'messages.txt'))
        create_file(Path(dirpath, 'cb_queries.txt'))

    def __init_user_log(self, user_id: int):
        logger.info('Initializing %s user log' % user_id)
        dirpath = self.get_user_log_dir(user_id)
        mkdir(dirpath)
        create_file(Path(dirpath, 'updates.txt'))
        fp = open_file(Path(dirpath, 'latest_update.json'), 'w')
        fp.write('{}')
        fp.close()

    def __handle_user_update(self, user: types.User):
        "Logs user profile updates"

        logger.info('Handling %s user update' % user.id)
        user_dir = self.get_user_log_dir(user.id)
        user_dict = user.__dict__
        latest_update_path = Path(user_dir, 'latest_update.json')
        updates_path = Path(user_dir, 'updates.txt')

        # Reading an old user update to compare with the new one
        fp = open_file(latest_update_path, 'r', encoding='utf8')
        logger.debug('Reading user update json file')
        latest_update = json.load(fp)
        fp.close()

        # Checks if any user fields have been updated
        upd = {}
        for field in user_dict:
            if not field in latest_update or user_dict[field] != latest_update[field]:
                upd[field] = user_dict[field]

        # If the user profile is updated, write the new changes
        if upd:
            # Record the full update
            logger.info('User profile updated, recording update...')
            fp = open_file(latest_update_path, 'w', encoding='utf8')
            logger.debug('Recording the full user profile')
            json.dump(user_dict, fp, ensure_ascii=False, indent=4)
            fp.close()

            # Record only updated fields
            fp = open_file(updates_path, 'a', encoding='utf8')
            logger.debug('Recording only updated fields...')
            fp.write('[{time}] {update}'.format(
                time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                update=json.dumps(upd, ensure_ascii=False)
            ).replace('\n', '\\n') + '\n')
            fp.close()
        else:
            logger.info('No user profile updates detected')

    def __handle_message(self, message: types.Message):
        "Logs messages, usually commands"

        logger.info('Handling message')
        chat_dir = Path(self.__dirpath, 'chats', str(message.chat.id))

        # Escape line breaks from message
        if message.text is not None:
            msg_text = message.text.replace('\n', '\\n')
        else:
            msg_text = None

        # Saving a message to the logs
        fp = open_file(Path(chat_dir, 'messages.txt'), 'a', encoding='utf8')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id} ({content_type}): {text}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message_id=message.message_id,
            content_type=message.content_type,
            text=msg_text
        ))
        fp.close()

    def __handle_callback_query(self, call: types.CallbackQuery):
        "Logs callback queries"

        logger.info('Handling callback query %s' % call.data)
        chat_dir = Path(self.__dirpath, 'chats', str(call.message.chat.id))

        # Saving a callback query to the logs
        fp = open_file(Path(chat_dir, 'cb_queries.txt'), 'a')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {data}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=call.message.chat.id,
            user_id=call.from_user.id,
            message_id=call.message.message_id,
            data=call.data
        ))
        fp.close()



    def message_middleware(self, bot: TeleBot, message: types.Message):
        "Message middleware handler"
        logger.info('Handling message from chat %s' % message.chat.id)

        if not self.__chat_log_initialized(message.chat.id):
            self.__init_chat_log(message.chat.id)

        if not self.__user_log_initialized(message.from_user.id):
            self.__init_user_log(message.from_user.id)

        self.__handle_message(message)
        self.__handle_user_update(message.from_user)

    def callback_query_middleware(self, bot: TeleBot, call: types.CallbackQuery):
        "Callback query middleware handler"
        logger.info('Handling callback query from chat %s' % call.message.chat.id)

        if not self.__chat_log_initialized(call.message.chat.id):
            self.__init_chat_log(call.message.chat.id)

        if not self.__user_log_initialized(call.from_user.id):
            self.__init_user_log(call.from_user.id)

        self.__handle_callback_query(call)
        self.__handle_user_update(call.from_user)
