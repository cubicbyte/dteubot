import os
import sys
import logging
from datetime import timedelta
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from .utils import check_int

sys.path.append('../../lib')                # Required to load external libraries
load_dotenv('.env')                         # Load .env file in current dir
load_dotenv()                               # Load .env file in bot dir


# Set environment variable default values
os.environ.setdefault('MODE', 'prod')
os.environ.setdefault('DEFAULT_LANG', 'en')
os.environ.setdefault('API_REQUEST_TIMEOUT', '-1')
os.environ.setdefault('API_CACHE_EXPIRES', '-1')
os.environ.setdefault('LOGGING_LEVEL', 'INFO')

# Validate environment variables
assert os.getenv('MODE') in ('prod', 'dev'), 'The MODE environment variable must be only prod or dev. Received: %s' % os.getenv('MODE')
assert os.getenv('LOGGING_LEVEL') in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), 'The LOGGING_LEVEL environment variable has an invalid value. Received: %s' % os.getenv('LOGGING_LEVEL')
assert check_int(os.getenv('API_REQUEST_TIMEOUT')), 'The API_REQUEST_TIMEOUT environment variable must be an integer. Received: %s' % os.getenv('API_REQUEST_TIMEOUT')
assert check_int(os.getenv('API_CACHE_EXPIRES')), 'The API_CACHE_EXPIRES environment variable must be an integer. Received: %s' % os.getenv('API_CACHE_EXPIRES')


BOT_TOKEN = os.getenv('BOT_TOKEN')
API_URL = os.getenv('API_URL')
DEFAULT_LANG = os.getenv('DEFAULT_LANG')
API_REQUEST_TIMEOUT = int(os.getenv('API_REQUEST_TIMEOUT'))
API_CACHE_EXPIRES = int(os.getenv('API_CACHE_EXPIRES'))
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL')
MODE = os.getenv('MODE')
LOG_CHAT_ID = os.getenv('LOG_CHAT_ID')

USER_DATA_PATH = 'user-data'
CHAT_DATA_PATH = 'chat-data'
LANGS_PATH = os.path.join(sys.path[0], 'langs')
LOGS_PATH = 'logs'
CACHE_PATH = 'cache'
API_TYPE_CACHED = 'CachedApi'
API_TYPE_DEFAULT = 'Api'

if API_REQUEST_TIMEOUT <= 0:
    API_REQUEST_TIMEOUT = None


os.makedirs(LOGS_PATH, exist_ok=True)
os.makedirs(USER_DATA_PATH, exist_ok=True)
os.makedirs(CHAT_DATA_PATH, exist_ok=True)


logging.basicConfig(
    level=LOGGING_LEVEL,
    filename=os.path.join(LOGS_PATH, 'debug.log'),
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    force=True
)

_logger = logging.getLogger(__name__)
_logger.info('Running setup')


from lib.api import Api
from lib.api.cached import CachedApi
from .tg_logger import TelegramLogger
from .load_langs import load_langs



if os.path.isfile(os.path.join(CACHE_PATH, 'mkr-cache.sqlite')):
    API_TYPE = API_TYPE_CACHED
    _Api = CachedApi
else:
    API_TYPE = API_TYPE_DEFAULT
    _Api = Api

bot = ApplicationBuilder().token(BOT_TOKEN).build()
api = _Api(
    url=API_URL,
    timeout=API_REQUEST_TIMEOUT,
    expires_after=timedelta(seconds=API_CACHE_EXPIRES),
    cache_name=os.path.join(CACHE_PATH, 'http-cache'))
tg_logger = TelegramLogger(os.path.join(LOGS_PATH, 'telegram'))
langs = load_langs(LANGS_PATH)
