import os
from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler, validate_admin


@register_button_handler('^admin.clear_logs$')
@validate_admin
async def handler(upd: Update, ctx: CallbackContext):
    # Clear logs file
    open(os.path.join(os.getenv('LOGS_PATH'), 'debug.log'), 'w').close()

    await upd.callback_query.answer(
        text=ctx._chat_data.get_lang()['alert.done'],
        show_alert=True
    )
