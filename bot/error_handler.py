import logging
import traceback
from datetime import datetime
from telegram import Update, Bot
from telegram.error import BadRequest, TelegramError, NetworkError, Forbidden
from telegram.ext import ContextTypes
from .data import ChatData
from .utils.smart_split import smart_split

_logger = logging.getLogger(__name__)
log_chat_id: int | str = None

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(context.error, BadRequest):
        _logger.warn(context.error)
        if context.error.message.startswith('Message is not modified'):
            return
        if context.error.message.startswith('Chat not found') or \
                context.error.message.startswith('Peer_id_invalid'):
            _chat_data = ChatData(update.effective_chat.id) # For some reason context._chat_data is None
            _chat_data.set('_accessible', False)
            return

    if isinstance(context.error, Forbidden):
        # Bot was blocked by the user
        _logger.warn(context.error)
        _chat_data = ChatData(update.effective_chat.id)
        _chat_data.set('_accessible', False)
        return

    if isinstance(context.error, NetworkError) and context.error.message.startswith('httpx'):
        # telegram.ext._updater already logs this error
        return

    if not isinstance(context.error, TelegramError):
        print(traceback.format_exc())

    _logger.exception(context.error)
    await _send_error(context.bot, context.error)

async def _send_error(bot: Bot, e: Exception):
    if log_chat_id is not None:
        for err_text in smart_split(f'[{datetime.now()}] {traceback.format_exc()}'):
            try:
                await bot.send_message(chat_id=log_chat_id, text=err_text)
            except:
                _logger.exception('Failed to send exception to log chat')
