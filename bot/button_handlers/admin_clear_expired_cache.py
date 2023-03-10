from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..settings import api, _Api, Api

@register_button_handler(r'^admin.clear_expired_cache$')
async def handler(update: Update, context: CallbackContext):
    if _Api == Api:
        api._session.remove_expired_responses()
    await update.callback_query.answer(
        text=context._chat_data.lang['alert.done'],
        show_alert=True
    )
