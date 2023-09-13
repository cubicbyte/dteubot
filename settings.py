"""
Bot settings
"""

import os
import sys
import logging

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from lib.api import CachedApi
from lib.teacher_loader.finder import TeacherFinder
from bot import utils
from bot.utils.lang import load_langs


# Constants
NOTIFICATIONS_SUGGESTION_DELAY_S = 60 * 60  # 1 hour, 3600 secs
TELEGRAM_SUPPORTED_HTML_TAGS = [
    'a', 's', 'i', 'b', 'u', 'em', 'pre',
    'ins', 'del', 'code', 'strong',
    'strike', 'tg-emoji']


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
assert utils.validate_bot_token(os.getenv('BOT_TOKEN', '')), \
    'The BOT_TOKEN environment variable is not set'

assert os.getenv('LOGGING_LEVEL') in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), \
    'The LOGGING_LEVEL environment variable has an invalid value. ' \
    + f'Received: {os.getenv("LOGGING_LEVEL")}'

assert utils.isfloat(os.getenv('API_REQUEST_TIMEOUT')), \
    'The API_REQUEST_TIMEOUT environment variable must be an float. ' \
    + f'Received: {os.getenv("API_REQUEST_TIMEOUT")}'

assert utils.isint(os.getenv('API_CACHE_EXPIRES')), \
    'The API_CACHE_EXPIRES environment variable must be an integer. ' \
    + f'Received: {os.getenv("API_CACHE_EXPIRES")}'


if float(os.getenv('API_REQUEST_TIMEOUT')) <= 0:
    os.environ.pop('API_REQUEST_TIMEOUT', None)
    API_REQUEST_TIMEOUT = None
else:
    API_REQUEST_TIMEOUT = float(os.getenv('API_REQUEST_TIMEOUT'))


TEACHERS_FILEPATH = os.path.join(os.getenv('CACHE_PATH'), 'teachers.csv')
LOGS_PATH = os.path.join(os.getenv('LOGS_PATH'), 'debug.log')

# Create directories
os.makedirs(os.getenv('CACHE_PATH'), exist_ok=True)
os.makedirs(os.getenv('LOGS_PATH'), exist_ok=True)
os.makedirs(os.getenv('LANGS_PATH'), exist_ok=True)
os.makedirs(os.getenv('USER_DATA_PATH'), exist_ok=True)
os.makedirs(os.getenv('CHAT_DATA_PATH'), exist_ok=True)


# Configure logging
logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),
    filename=os.path.join(os.getenv('LOGS_PATH'), 'debug.log'),
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    force=True,
    encoding='utf-8'
)
if os.getenv('LOGGING_LEVEL') == 'INFO':
    # Disable every http request logging
    logging.getLogger('httpx').setLevel('WARNING')

_logger = logging.getLogger(__name__)
_logger.info('Initializing bot settings')


# Init teacher finder (allows users to click teacher's name in schedule)
if os.path.exists(TEACHERS_FILEPATH):
    _logger.info('Loading teachers list from %s', TEACHERS_FILEPATH)
    teacher_finder = TeacherFinder(TEACHERS_FILEPATH)
else:
    _logger.warning('Teachers list is not loaded. Run scripts/load_teachers.py to load it.')
    teacher_finder = None


langs = load_langs(os.getenv('LANGS_PATH'))
bot = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()

api = CachedApi(
    url=os.getenv('API_URL'),
    timeout=API_REQUEST_TIMEOUT,
    cache_expires=int(os.getenv('API_CACHE_EXPIRES')),
    cache_path=os.path.join(os.getenv('CACHE_PATH'), 'api-cache.sqlite'),
    cache_name=os.path.join(os.getenv('CACHE_PATH'), 'http-cache')
)

# Sort languages (1. Ukrainian, 2. English, 3+ - Other)
langs_ = {}
if 'uk' in langs:
    langs_['uk'] = langs.pop('uk')
if 'en' in langs:
    langs_['en'] = langs.pop('en')
langs_.update(langs)
langs = langs_
