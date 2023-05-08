from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import menu
from bot.utils import parse_callback_query
from bot.data import Message


@register_button_handler('^select.schedule.group')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']

    group_id = int(args['groupId'])
    context._chat_data.set('group_id', group_id)

    msg = await update.callback_query.edit_message_text(
        **menu.create_message(context))

    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'menu',
                context._chat_data.get('lang_code')))
