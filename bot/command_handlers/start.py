from telegram import Update
from telegram.ext import ContextTypes
from bot.command_handlers import register_command_handler
from bot.pages import greeting, structure_list
from bot.data import Message


@register_command_handler('start')
async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Set referral link
    if len(context.args) == 0:
        ref = None
    else:
        ref = context.args[0]

    if context._user_data.get('ref') is None:
        context._user_data.set('ref', ref)

    # Send greeting message
    msg = await update.message.chat.send_message(**greeting.create_message(context))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'greeting', context._chat_data.get('lang_code')))

    # Send main message
    msg = await update.message.chat.send_message(**structure_list.create_message(context))
    context._chat_data.add_message(
        Message(msg.message_id, msg.date, 'structure_list', context._chat_data.get('lang_code')))
