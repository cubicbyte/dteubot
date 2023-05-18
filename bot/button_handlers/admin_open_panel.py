from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler, validate_admin
from bot.pages import admin_panel


@register_button_handler('^admin.open_panel$')
@validate_admin
async def handler(upd: Update, ctx: CallbackContext):
    msg = await upd.callback_query.edit_message_text(**admin_panel.create_message(ctx))
    ctx._chat_data.save_message('admin_panel', msg)
