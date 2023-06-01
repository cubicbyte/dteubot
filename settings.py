import os
import sys
import logging
from datetime import timedelta
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot.utils import check_int

# Load environment variable files (.env)
sys.path.append('../../lib')  # Required to load external libraries
load_dotenv('.env')           # Load .env file in current dir
load_dotenv()                 # Load .env file in bot dir

# Set environment variable default values
os.environ.setdefault('DEFAULT_LANG', 'en')
os.environ.setdefault('API_REQUEST_TIMEOUT', '-1')
os.environ.setdefault('API_CACHE_EXPIRES', '-1')
os.environ.setdefault('LOGGING_LEVEL', 'INFO')
os.environ.setdefault('USER_DATA_PATH', 'user-data')
os.environ.setdefault('CHAT_DATA_PATH', 'chat-data')
os.environ.setdefault('LOGS_PATH', 'logs')
os.environ.setdefault('CACHE_PATH', 'cache')
os.environ.setdefault('LANGS_PATH', os.path.join(sys.path[0], 'langs'))

# Validate environment variables
assert os.getenv('LOGGING_LEVEL') in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), 'The LOGGING_LEVEL environment variable has an invalid value. Received: %s' % os.getenv('LOGGING_LEVEL')
assert check_int(os.getenv('API_REQUEST_TIMEOUT')), 'The API_REQUEST_TIMEOUT environment variable must be an integer. Received: %s' % os.getenv('API_REQUEST_TIMEOUT')
assert check_int(os.getenv('API_CACHE_EXPIRES')), 'The API_CACHE_EXPIRES environment variable must be an integer. Received: %s' % os.getenv('API_CACHE_EXPIRES')


if int(os.getenv('API_REQUEST_TIMEOUT')) <= 0:
    os.environ.update(API_REQUEST_TIMEOUT=None)


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


from lib.api import Api
from lib.api.cached import CachedApi
from bot.tg_logger import TelegramLogger


# Use CachedApi if possible
_cache_exists = os.path.isfile(os.path.join(os.getenv('CACHE_PATH'), 'mkr-cache.sqlite'))
_Api = CachedApi if _cache_exists else Api
API_TYPE_CACHED = 'CachedApi'
API_TYPE_DEFAULT = 'Api'
API_TYPE = API_TYPE_CACHED if _cache_exists else API_TYPE_DEFAULT


bot = ApplicationBuilder().token(os.getenv('BOT_TOKEN')).build()
tg_logger = TelegramLogger(os.path.join(os.getenv('LOGS_PATH'), 'telegram'))

api = _Api(
    url=os.getenv('API_URL'),
    enable_cache=True,
    timeout=int(os.getenv('API_REQUEST_TIMEOUT')),
    expire_after=timedelta(seconds=int(os.getenv('API_CACHE_EXPIRES'))),
    cache_name=os.path.join(os.getenv('CACHE_PATH'), 'http-cache')
)
