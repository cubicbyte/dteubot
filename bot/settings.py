import os
import sys
import logging
from datetime import timedelta
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from .utils.check_int import check_int

USER_DATA_PATH = 'user-data'
CHAT_DATA_PATH = 'chat-data'
LANGS_PATH = os.path.join(sys.path[0], 'langs')
LOGS_PATH = 'logs'
#TODO DEFAULT_LANG = ..., LOGGING_LEVEL = ..., ...

sys.path.append('../../lib')                # Required to load external libraries
sys.path.append('../../scripts')            # Required to load external scripts
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


os.makedirs(LOGS_PATH, exist_ok=True)
os.makedirs(USER_DATA_PATH, exist_ok=True)
os.makedirs(CHAT_DATA_PATH, exist_ok=True)


logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),
    filename=os.path.join(LOGS_PATH, 'debug.log'),
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    force=True
)

logger = logging.getLogger(__name__)
logger.info('Running setup')


from lib.api import Api, CachedApi
from scripts.update_bot_data import main as update_bot_data
#from .exception_handler import ExceptionHandler
from .tg_logger import TelegramLogger
from .load_langs import load_langs



BOT_TOKEN = os.getenv('BOT_TOKEN')
api_url = os.getenv('API_URL')
api_timeout = int(os.getenv('API_REQUEST_TIMEOUT'))
api_expires = timedelta(seconds=int(os.getenv('API_CACHE_EXPIRES')))

if api_timeout <= 0:
    api_timeout = None

if os.path.isfile('cache/mkr-cache.sqlite'):
    _Api = CachedApi
else:
    _Api = Api

update_bot_data('.')
logger.info('Creating a bot instance')
bot = ApplicationBuilder().token(BOT_TOKEN).build()
#bot.exception_handler = ExceptionHandler(bot=bot, log_chat_id=os.getenv('LOG_CHAT_ID')) #TODO
api = _Api(url=api_url, timeout=api_timeout, expires_after=api_expires)
tg_logger = TelegramLogger(os.path.join(LOGS_PATH, 'telegram'))
langs = load_langs(LANGS_PATH)
