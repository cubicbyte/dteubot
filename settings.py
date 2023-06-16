"""
Bot settings
"""

import os
import sys
from datetime import timedelta

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from lib.api import Api
from bot.utils import isint, isfloat


# Constants
NOTIFICATIONS_SUGGESTION_DELAY_S = 60 * 60 * 24 * 3  # 3 days, 259,200 seconds
TELEGRAM_SUPPORTED_HTML_TAGS = [
    'a', 's', 'i', 'b', 'u', 'em', 'pre',
    'ins', 'del', 'span', 'code', 'strong',
    'strike', 'tg-spoiler', 'tg-emoji']


# Load environment variable files (.env)
load_dotenv('.env')  # Load .env file in current dir
load_dotenv()        # Load .env file in bot dir


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


if float(os.getenv('API_REQUEST_TIMEOUT')) <= 0:
    os.environ.pop('API_REQUEST_TIMEOUT', None)
    API_REQUEST_TIMEOUT = None
else:
    API_REQUEST_TIMEOUT = float(os.getenv('API_REQUEST_TIMEOUT'))


bot = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

api = Api(
    url=os.getenv('API_URL'),
    enable_cache=True,
    timeout=API_REQUEST_TIMEOUT,
    raw_result=True,
    expire_after=timedelta(seconds=int(os.getenv('API_CACHE_EXPIRES'))),
    cache_name=os.path.join(os.getenv('CACHE_PATH'), 'http-cache')
)
