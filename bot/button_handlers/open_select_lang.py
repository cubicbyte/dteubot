from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import lang_selection
from bot.data import Message


@register_button_handler('^open.select_lang$')
async def handler(update: Update, context: CallbackContext):
    msg = await update.callback_query.edit_message_text(**lang_selection.create_message(context))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'lang_selection', context._chat_data.get('lang_code')))
