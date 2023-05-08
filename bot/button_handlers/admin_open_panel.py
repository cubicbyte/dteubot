from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler, validate_admin
from bot.pages import admin_panel
from bot.data import Message


@register_button_handler('^admin.open_panel$')
@validate_admin
async def handler(update: Update, context: CallbackContext):
    msg = await update.callback_query.edit_message_text(**admin_panel.create_message(context))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'admin_panel', context._chat_data.get('lang_code')))
