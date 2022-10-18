from asyncio.log import logger
import os
import sys
import telebot
import logging
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

sys.path.append('../lib')
load_dotenv()
os.environ.setdefault('MODE', 'prod')
os.chdir(sys.path[0])
telebot.apihelper.ENABLE_MIDDLEWARE = True

if not os.path.exists('logs'):
    os.mkdir('logs')

if not os.path.exists('logs/debug'):
    os.mkdir('logs/debug')

logging.basicConfig(
    level=os.getenv('LOGGING_LEVEL'),
    filename=os.path.join(os.getcwd(), 'logs', 'debug', '%s.log' % datetime.now().strftime('%Y-%m-%d %H-%M-%S')),
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



bot_token = os.getenv('BOT_TOKEN')
chat_configs_path = Path('chat-configs').absolute()
tg_logs_path = Path('logs/telegram').absolute()

bot = telebot.TeleBot(bot_token)
api = Api(url=os.getenv('API_URL'), timeout=int(os.getenv('API_REQUEST_TIMEOUT')))
tg_logger = TelegramLogger(tg_logs_path)
chat_configs = ChatConfigs(chat_configs_path)
langs = load_langs('langs')
