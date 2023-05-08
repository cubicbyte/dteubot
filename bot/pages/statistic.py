import os.path
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
from settings import tg_logger


def create_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> dict:
    chat_dir = tg_logger.get_chat_log_dir(update.effective_chat.id)

    # Get first message date and message count
    with open(os.path.join(chat_dir, 'messages.txt')) as fp:
        for messages, line in enumerate(fp):
            if messages == 0:
                first_msg_date = line[1:line.index(']')]

    # Get number of button clicks
    with open(os.path.join(chat_dir, 'cb_queries.txt')) as fp:
        for clicks, _ in enumerate(fp):
            pass

    message_text = '*Statistic*\n\nThis chat ID: {chat_id}\nYour ID: {user_id}\nMessages: {messages}\nButton clicks: {clicks}\nFirst message: {first}'.format(
        chat_id=update.effective_chat.id,
        user_id=update.effective_user.id,
        messages=messages,
        clicks=clicks,
        first=escape_markdown(first_msg_date, version=2)
    )

    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.menu'],
                             callback_data='open.menu'),
        InlineKeyboardButton(text='How Did We Get Here?',
                             url='https://github.com/cubicbyte/dteubot')
    ]]

    return {
        'text': message_text,
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
