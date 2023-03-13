from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler, validate_admin
from ..settings import api, API_TYPE, API_TYPE_DEFAULT

@register_button_handler(r'^admin.clear_all_cache$')
@validate_admin
async def handler(update: Update, context: CallbackContext):
    if API_TYPE == API_TYPE_DEFAULT:
        api._session.remove_expired_responses(expire_after=1)
    await update.callback_query.answer(
        text=context._chat_data.get_lang()['alert.done'],
        show_alert=True
    )
