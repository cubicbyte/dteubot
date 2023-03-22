from telegram import Update
from telegram.ext import CallbackContext
from . import register_button_handler
from ..pages import settings
from ..utils import parse_callback_query
from ..data import Message

@register_button_handler('^set.cl_notif_1m')
async def handler(update: Update, context: CallbackContext):
    args = parse_callback_query(update.callback_query.data)['args']
    state = args.get('state') == '1'
    suggestion = args.get('suggestion') == '1'
    context._chat_data.set('cl_notif_1m', state)

    if state:
        context._chat_data.set('cl_notif_15m', False)

    if suggestion:
        await update.callback_query.answer(context._chat_data.get_lang()['alert.cl_notif_enabled_tooltip'].format(remaining='1'), show_alert=True)
        await update.callback_query.delete_message()
        context._chat_data.remove_message(update.callback_query.message.message_id)
        return

    msg = await update.callback_query.edit_message_text(**settings.create_message(context))
    context._chat_data.add_message(Message(msg.message_id, msg.date, 'settings', context._chat_data.get('lang_code')))
