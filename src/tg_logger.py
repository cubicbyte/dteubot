import os
import logging
import json

from datetime import datetime
from pathlib import Path
from telebot import types, TeleBot


logger = logging.getLogger()


class TelegramLogger:
    def __init__(self, dirpath):
        logger.debug('Creating TelegramLogger instance')

        self.__dirpath = dirpath
        self.__init_dirs()

    def get_chat_log_dir(self, chat_id: int) -> Path:
        return Path(self.__dirpath, 'chats', str(chat_id))

    def get_user_log_dir(self, user_id: int) -> Path:
        return Path(self.__dirpath, 'users', str(user_id))

    def __init_dirs(self):
        logging.debug('Initialising TelegramLogger dirs')

        if not os.path.exists(self.__dirpath):
            os.mkdir(self.__dirpath)

        if not os.path.exists(Path(self.__dirpath, 'chats')):
            os.mkdir(Path(self.__dirpath, 'chats'))

        if not os.path.exists(Path(self.__dirpath, 'users')):
            os.mkdir(Path(self.__dirpath, 'users'))

    def __chat_log_initialized(self, chat_id: int) -> bool:
        return os.path.exists(self.get_chat_log_dir(chat_id))

    def __user_log_initialized(self, user_id: int) -> bool:
        return os.path.exists(self.get_user_log_dir(user_id))

    def __init_chat_log(self, chat_id: int):
        logger.debug('Initialising %s chat log' % chat_id)

        chat_dir = self.get_chat_log_dir(chat_id)
        os.mkdir(chat_dir)

        open(Path(chat_dir, 'messages.txt'), 'w').close()
        open(Path(chat_dir, 'cb_queries.txt'), 'w').close()

    def __init_user_log(self, user_id: int):
        logger.debug('Initialising %s user log' % user_id)

        user_dir = self.get_user_log_dir(user_id)
        os.mkdir(user_dir)

        open(Path(user_dir, 'updates.txt'), 'w').close()

        fp = open(Path(user_dir, 'latest_update.json'), 'w')
        fp.write('{}')
        fp.close()

    def __handle_user_update(self, user: types.User):
        user_dir = self.get_user_log_dir(user.id)
        user_dict = user.__dict__

        latest_update_path = Path(user_dir, 'latest_update.json')
        updates_path = Path(user_dir, 'updates.txt')

        file = open(latest_update_path, 'r', encoding='utf8')
        latest_update = json.load(file)
        file.close()

        upd = {}
        for field in user_dict:
            if not field in latest_update or user_dict[field] != latest_update[field]:
                upd[field] = user_dict[field]

        if upd:
            file = open(latest_update_path, 'w', encoding='utf8')
            json.dump(user_dict, file, ensure_ascii=False, indent=4)
            file.close()
            
            file2 = open(updates_path, 'a', encoding='utf8')
            file2.write('[{time}] {update}'.format(
                time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                update=json.dumps(upd, ensure_ascii=False)
            ).replace('\n', '\\n') + '\n')
            file2.close()

        file.close()

    def __handle_message(self, message: types.Message):
        chat_dir = Path(self.__dirpath, 'chats', str(message.chat.id))

        if message.text is not None:
            msg_text = message.text.replace('\n', '\\n')
        else:
            msg_text = None
        
        file = open(Path(chat_dir, 'messages.txt'), 'a')
        file.write('[{time}] {chat_id}/{user_id}/{message_id} ({content_type}): {text}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            message_id=message.id,
            content_type=message.content_type,
            text=msg_text
        ))
        file.close()

    def __handle_callback_query(self, call: types.CallbackQuery):
        chat_dir = Path(self.__dirpath, 'chats', str(call.message.chat.id))
        
        file = open(Path(chat_dir, 'cb_queries.txt'), 'a')
        file.write('[{time}] {chat_id}/{user_id}/{message_id}: {data}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=call.message.chat.id,
            user_id=call.from_user.id,
            message_id=call.message.id,
            data=call.data
        ))
        file.close()



    def message_middleware(self, bot: TeleBot, message: types.Message):
        logger.debug('Handling message from chat %s' % message.chat.id)

        if not self.__chat_log_initialized(message.chat.id):
            self.__init_chat_log(message.chat.id)

        if not self.__user_log_initialized(message.from_user.id):
            self.__init_user_log(message.from_user.id)

        self.__handle_message(message)
        self.__handle_user_update(message.from_user)

    def callback_query_middleware(self, bot: TeleBot, call: types.CallbackQuery):
        logger.debug('Handling callback query from chat %s' % call.message.chat.id)

        if not self.__chat_log_initialized(call.message.chat.id):
            self.__init_chat_log(call.message.chat.id)

        if not self.__user_log_initialized(call.from_user.id):
            self.__init_user_log(call.from_user.id)

        self.__handle_callback_query(call)
        self.__handle_user_update(call.from_user)
