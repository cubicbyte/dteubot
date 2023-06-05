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
        self._init_dirs()

    def get_chat_log_dir(self, chat_id: int) -> str:
        """Returns chat log dirpath"""
        return os.path.join(self._dirpath, 'chats', str(chat_id))

    def _init_dirs(self):
        logger.info('Initializing TelegramLogger dirs')
        os.makedirs(os.path.join(self._dirpath, 'chats'), exist_ok=True)

    def _chat_log_initialized(self, chat_id: int) -> bool:
        return os.path.exists(self.get_chat_log_dir(chat_id))

    def _init_chat_log(self, chat_id: int):
        logger.info('Initializing %s chat log' % chat_id)
        dirpath = self.get_chat_log_dir(chat_id)
        os.mkdir(dirpath)
        open(os.path.join(dirpath, 'messages.txt'), 'w').close()
        open(os.path.join(dirpath, 'cb_queries.txt'), 'w').close()

    def _save_message_to_logs(self, update: Update):
        # Escape line breaks
        if update.effective_message.text is not None:
            msg_text = update.effective_message.text.replace('\n', '\\n')
        else:
            msg_text = None

        file = os.path.join(self._dirpath, 'chats', str(update.effective_chat.id), 'messages.txt')
        fp = open(file, 'a')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {text}\n'.format(
            time=datetime.now().isoformat(sep=' ', timespec='seconds'),
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message_id=update.effective_message.id,
            text=msg_text
        ))
        fp.close()

    def _save_callback_query_to_logs(self, update: Update):
        file = os.path.join(self._dirpath, 'chats', str(update.effective_chat.id), 'cb_queries.txt')
        fp = open(file, 'a')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {data}\n'.format(
            time=datetime.now().isoformat(sep=' ', timespec='seconds'),
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message_id=update.effective_message.id,
            data=update.callback_query.data
        ))
        fp.close()

    async def message_handler(self, ctx):
        if not self._chat_log_initialized(ctx.update.effective_chat.id):
            self._init_chat_log(ctx.update.effective_chat.id)
        self._save_message_to_logs(ctx.update)

    async def callback_query_handler(self, ctx):
        if not self._chat_log_initialized(ctx.update.effective_chat.id):
            self._init_chat_log(ctx.update.effective_chat.id)
        self._save_callback_query_to_logs(ctx.update)
