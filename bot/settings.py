import os
import sys
import telebot
import logging
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

sys.path.append('../lib')                   # Required to load external api library
load_dotenv()                               # Load .env file
os.environ.setdefault('MODE', 'prod')
os.chdir(sys.path[0])                       # Run python in current directory
telebot.apihelper.ENABLE_MIDDLEWARE = True  # Enable telegram bot middleware

if not os.path.exists('./logs/'):
    os.mkdir('logs')

if not os.path.exists('./logs/debug/'):
    os.mkdir('logs/debug')

logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),
    filename='logs/debug/%s.log' % datetime.now().strftime('%Y-%m-%d %H-%M-%S'),
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    force=True
)

logger = logging.getLogger(__name__)
logger.info('Running setup')

from lib.api import Api
from .tg_logger import TelegramLogger
from .chat_configs import ChatConfigs
from .load_langs import load_langs



BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
api = Api(url=os.getenv('API_URL'), timeout=int(os.getenv('API_REQUEST_TIMEOUT')))
tg_logger = TelegramLogger('logs/telegram')
chat_configs = ChatConfigs('chat-configs')
langs = load_langs('langs')
