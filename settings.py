"""
Bot settings
"""

import os
import sys
import logging
from datetime import timedelta

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from bot.utils import isint, isfloat


NOTIFICATIONS_SUGGESTION_DELAY_S = 60 * 60 * 24 * 3  # 3 days, 259,200 seconds

TELEGRAM_SUPPORTED_HTML_TAGS = [
    'a', 's', 'i', 'b', 'u', 'em', 'pre',
    'ins', 'del', 'span', 'code', 'strong',
    'strike', 'tg-spoiler', 'tg-emoji'
]


# Load environment variable files (.env)
load_dotenv('.env')           # Load .env file in current dir
load_dotenv()                 # Load .env file in bot dir

# Set environment variable default values
os.environ.setdefault('DEFAULT_LANG', 'uk')
os.environ.setdefault('API_REQUEST_TIMEOUT', '-1')
os.environ.setdefault('API_CACHE_EXPIRES', '-1')
os.environ.setdefault('LOGGING_LEVEL', 'INFO')
os.environ.setdefault('USER_DATA_PATH', 'user-data')
os.environ.setdefault('CHAT_DATA_PATH', 'chat-data')
os.environ.setdefault('LOGS_PATH', 'logs')
os.environ.setdefault('CACHE_PATH', 'cache')
os.environ.setdefault('LANGS_PATH', os.path.join(sys.path[0], 'langs'))

# Validate environment variables
assert str(os.getenv('BOT_TOKEN')).strip() != '', \
    'The BOT_TOKEN environment variable is not set'

assert os.getenv('LOGGING_LEVEL') in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), \
    'The LOGGING_LEVEL environment variable has an invalid value. ' \
    + f'Received: {os.getenv("LOGGING_LEVEL")}'

assert isfloat(os.getenv('API_REQUEST_TIMEOUT')), \
    'The API_REQUEST_TIMEOUT environment variable must be an float. ' \
    + f'Received: {os.getenv("API_REQUEST_TIMEOUT")}'

assert isint(os.getenv('API_CACHE_EXPIRES')), \
    'The API_CACHE_EXPIRES environment variable must be an integer. ' \
    + f'Received: {os.getenv("API_CACHE_EXPIRES")}'


# Create required directories
os.makedirs(os.getenv('LOGS_PATH'), exist_ok=True)
os.makedirs(os.getenv('USER_DATA_PATH'), exist_ok=True)
os.makedirs(os.getenv('CHAT_DATA_PATH'), exist_ok=True)


logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),
    filename=os.path.join(os.getenv('LOGS_PATH'), 'debug.log'),
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    force=True
)

_logger = logging.getLogger(__name__)
_logger.info('Running setup')


# pylint: disable=wrong-import-position
from bot.logger import TelegramLogger
from lib.api import Api


# Use CachedApi if possible
_ApiClass = Api
API_TYPE_CACHED = 'CachedApi'
API_TYPE_DEFAULT = 'Api'
API_TYPE = API_TYPE_DEFAULT

if float(os.getenv('API_REQUEST_TIMEOUT')) <= 0:
    os.environ.pop('API_REQUEST_TIMEOUT', None)
    API_REQUEST_TIMEOUT = None
else:
    API_REQUEST_TIMEOUT = float(os.getenv('API_REQUEST_TIMEOUT'))


bot = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()
tg_logger = TelegramLogger(os.path.join(os.getenv('LOGS_PATH'), 'telegram'))
langs: dict = {}

api = _ApiClass(
    url=os.getenv('API_URL'),
    enable_cache=True,
    timeout=API_REQUEST_TIMEOUT,
    raw_result=True,
    expire_after=timedelta(seconds=int(os.getenv('API_CACHE_EXPIRES'))),
    cache_name=os.path.join(os.getenv('CACHE_PATH'), 'http-cache')
)
