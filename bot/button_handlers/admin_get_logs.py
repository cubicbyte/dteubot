import os
from telegram import Update
from telegram.ext import CallbackContext
from bot.button_handlers import register_button_handler, validate_admin


@register_button_handler('^admin.get_logs$')
@validate_admin
async def handler(upd: Update, ctx: CallbackContext):
    # Show user that bot is sending file
    await ctx.bot.send_chat_action(upd.callback_query.message.chat.id, 'upload_document')

    # Read and send logs file
    filepath = os.path.join(LOGS_PATH, 'debug.log')
    with open(filepath, 'rb') as file:
        await ctx.bot.send_document(upd.callback_query.message.chat.id, file)
