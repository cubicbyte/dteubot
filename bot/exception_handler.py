import logging
import traceback
from datetime import datetime
from requests.exceptions import ConnectionError
from telebot import ExceptionHandler as _ExceptionHandler, TeleBot
from telebot.apihelper import ApiException
from telebot.util import smart_split

logger = logging.getLogger(__name__)

class TelegramException:
    MESSAGE_NOT_MODIFIED = 'Bad Request: message is not modified'

class ExceptionHandler(_ExceptionHandler):
    """
    Class for handling exceptions while Polling
    """

    def __init__(self, bot: TeleBot = None, log_chat_id: int | str = None):
        self.bot = bot
        self.log_chat_id = log_chat_id

    def _log_exception(self, e: Exception):
        if self.bot is not None and self.log_chat_id is not None:
            for err_text in smart_split(f'[{datetime.now()}] {traceback.format_exc()}'):
                try:
                    self.bot.send_message(self.log_chat_id, err_text)
                except ApiException:
                    logger.exception('Failed to send exception to log chat')

    def handle(self, e):
        if isinstance(e, ConnectionError):
            logger.exception('Connection error')
            return True

        if isinstance(e, ApiException):
            if e.description.startswith(TelegramException.MESSAGE_NOT_MODIFIED):
                logger.warn('Message not modified')
                return True

        logger.exception(e)
        self._log_exception(e)
        return True
