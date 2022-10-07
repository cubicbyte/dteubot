import os
import logging

from datetime import datetime
from pathlib import Path
from telebot import types, TeleBot


logger = logging.getLogger()


class TelegramLogger:
    def __init__(self, dirpath) -> None:
        logger.debug('Creating TelegramLogger instance')

        self.__dirpath = dirpath
        self.__init_dirs()

    def get_chat_config_dir(self, chat_id: int) -> Path:
        return Path(self.__dirpath, 'chats', str(chat_id))

    def __init_dirs(self) -> None:
        logging.debug('Initialising TelegramLogger dirs')

        if not os.path.exists(self.__dirpath):
            os.mkdir(self.__dirpath)

        if not os.path.exists(Path(self.__dirpath, 'chats')):
            os.mkdir(Path(self.__dirpath, 'chats'))

    def __chat_log_initialized(self, chat_id: int) -> bool:
        return os.path.exists(self.get_chat_config_dir(chat_id))

    def __init_chat_log(self, chat_id: int) -> None:
        logger.debug('Initialising %s chat log' % chat_id)

        chat_dir = Path(self.__dirpath, 'chats', str(chat_id))
        os.mkdir(chat_dir)

        open(Path(chat_dir, 'messages.txt'), 'w').close()
        open(Path(chat_dir, 'cb_queries.txt'), 'w').close()

    def __handle_message(self, message: types.Message) -> None:
        chat_dir = Path(self.__dirpath, 'chats', str(message.chat.id))

        if message.text is not None:
            msg_text = msg_text.replace('\n', '\\n')
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

    def __handle_callback_query(self, call: types.CallbackQuery) -> None:
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



    def message_middleware(self, bot: TeleBot, message: types.Message) -> None:
        logger.debug('Handling message from chat %s' % message.chat.id)

        if not self.__chat_log_initialized(message.chat.id):
            self.__init_chat_log(message.chat.id)

        self.__handle_message(message)

    def callback_query_middleware(self, bot: TeleBot, call: types.CallbackQuery) -> None:
        logger.debug('Handling callback query from chat %s' % call.message.chat.id)

        if not self.__chat_log_initialized(call.message.chat.id):
            self.__init_chat_log(call.message.chat.id)

        self.__handle_callback_query(call)
