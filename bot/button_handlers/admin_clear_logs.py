import os.path
from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..settings import LOGS_PATH

@register_button_handler(r'^admin.clear_logs$')
async def handler(update: Update, context: CallbackContext):
    open(os.path.join(LOGS_PATH, 'debug.log'), 'w').close()
    await update.callback_query.answer(
        text=context._chat_data.lang['alert.done'],
        show_alert=True
    )
