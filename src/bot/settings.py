import os
import sys
import telebot
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

CHAT_CONFIGS_PATH = 'chat-configs'
LANGS_PATH = 'langs'
LOGS_PATH = 'logs'

sys.path.append('../../lib')                # Required to load external libraries
sys.path.append('../../scripts')            # Required to load external scripts
load_dotenv('.env')                         # Load .env file in current dir
load_dotenv()                               # Load .env file in bot dir
telebot.apihelper.ENABLE_MIDDLEWARE = True  # Enable telegram bot middleware


# Set environment variable default values
os.environ.setdefault('MODE', 'prod')
os.environ.setdefault('DEFAULT_LANG', 'en')
os.environ.setdefault('API_REQUEST_TIMEOUT', '-1')
os.environ.setdefault('API_CACHE_EXPIRES', '-1')
os.environ.setdefault('LOGGING_LEVEL', 'INFO')

# Validate environment variables
assert os.getenv('MODE') in ('prod', 'dev'), 'The MODE environment variable must be only prod or dev. Received: %s' % os.getenv('MODE')
assert os.getenv('API_REQUEST_TIMEOUT').isdigit(), 'The API_REQUEST_TIMEOUT environment variable must be an integer. Received: %s' % os.getenv('API_REQUEST_TIMEOUT')
assert os.getenv('API_CACHE_EXPIRES').isdigit(), 'The API_CACHE_EXPIRES environment variable must be an integer. Received: %s' % os.getenv('API_CACHE_EXPIRES')
assert os.getenv('LOGGING_LEVEL') in ('NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), 'The LOGGING_LEVEL environment variable has an invalid value. Received: %s' % os.getenv('LOGGING_LEVEL')


if not os.path.exists(LOGS_PATH):
    os.mkdir(LOGS_PATH)

if not os.path.exists(os.path.join(LOGS_PATH, 'debug')):
    os.mkdir(os.path.join(LOGS_PATH, 'debug'))


logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),
    filename=os.path.join(LOGS_PATH, 'debug', '%s.log' % datetime.now().strftime('%Y-%m-%d %H-%M-%S')),
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    force=True
)

logger = logging.getLogger(__name__)
logger.info('Running setup')


from lib.api import Api
from scripts.update_chat_configs import main as update_chat_configs
from .tg_logger import TelegramLogger
from .chat_configs import ChatConfigs
from .load_langs import load_langs



BOT_TOKEN = os.getenv('BOT_TOKEN')
api_url = os.getenv('API_URL')
api_timeout = int(os.getenv('API_REQUEST_TIMEOUT'))
api_expires = timedelta(seconds=int(os.getenv('API_CACHE_EXPIRES')))

if api_timeout <= 0:
    api_timeout = None

update_chat_configs(CHAT_CONFIGS_PATH)
bot = telebot.TeleBot(BOT_TOKEN)
api = Api(url=api_url, timeout=api_timeout, expires_after=api_expires)
tg_logger = TelegramLogger(os.path.join(LOGS_PATH, 'telegram'))
chat_configs = ChatConfigs(CHAT_CONFIGS_PATH)
langs = load_langs(LANGS_PATH)
