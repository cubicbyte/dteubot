from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler
from bot.pages import settings
from bot.utils import parse_callback_query


@register_button_handler('^set.cl_notif_1m')
async def handler(upd: Update, ctx: CallbackContext):
    args = parse_callback_query(upd.callback_query.data)['args']

    state = args.get('state') == '1'
    suggestion = args.get('suggestion') == '1'
    ctx._chat_data.set('cl_notif_1m', state)

    # Disable 15m notifications if needed
    if state:
        ctx._chat_data.set('cl_notif_15m', False)

    # Show tooltip if needed
    if suggestion:
        await upd.callback_query.answer(
            ctx._chat_data.get_lang()['alert.cl_notif_enabled_tooltip']
                .format(remaining='1'), show_alert=True)
        await upd.callback_query.delete_message()
        ctx._chat_data.remove_message(upd.callback_query.message.message_id)
        return

    # Send message
    msg = await upd.callback_query.edit_message_text(
        **settings.create_message(ctx))
    ctx._chat_data.save_message('settings', msg)
