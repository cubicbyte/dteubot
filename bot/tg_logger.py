import os
import logging
from datetime import datetime
from telegram import Update

logger = logging.getLogger(__name__)


class TelegramLogger:
    """Logger to log messages/button clicks"""

    def __init__(self, dirpath):
        logger.debug('Creating TelegramLogger instance')

        self._dirpath = dirpath
        self.__init_dirs()

    def get_chat_log_dir(self, chat_id: int) -> str:
        """Returns chat log dirpath"""
        return os.path.join(self._dirpath, 'chats', str(chat_id))

    def __init_dirs(self):
        logger.info('Initializing TelegramLogger dirs')
        os.makedirs(os.path.join(self._dirpath, 'chats'), exist_ok=True)

    def __chat_log_initialized(self, chat_id: int) -> bool:
        return os.path.exists(self.get_chat_log_dir(chat_id))

    def __init_chat_log(self, chat_id: int):
        logger.info('Initializing %s chat log' % chat_id)
        dirpath = self.get_chat_log_dir(chat_id)
        os.mkdir(dirpath)
        open(os.path.join(dirpath, 'messages.txt'), 'w').close()
        open(os.path.join(dirpath, 'cb_queries.txt'), 'w').close()

    def __save_message_to_logs(self, update: Update):
        # Escape line breaks
        if update.effective_message.text is not None:
            msg_text = update.effective_message.text.replace('\n', '\\n')
        else:
            msg_text = None

        file = os.path.join(self._dirpath, 'chats', str(update.effective_chat.id), 'messages.txt')
        fp = open(file, 'a')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {text}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message_id=update.effective_message.id,
            text=msg_text
        ))
        fp.close()

    def __save_callback_query_to_logs(self, update: Update):
        file = os.path.join(self._dirpath, 'chats', str(update.effective_chat.id), 'cb_queries.txt')
        fp = open(file, 'a')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {data}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message_id=update.effective_message.id,
            data=update.callback_query.data
        ))
        fp.close()

    async def message_handler(self, update: Update, ctx):
        if not self.__chat_log_initialized(update.effective_chat.id):
            self.__init_chat_log(update.effective_chat.id)
        self.__save_message_to_logs(update)

    async def callback_query_handler(self, update: Update, ctx):
        if not self.__chat_log_initialized(update.effective_chat.id):
            self.__init_chat_log(update.effective_chat.id)
        self.__save_callback_query_to_logs(update)
