from telebot import types
from ..settings import tg_logger

def create_message(message: types.Message) -> dict:
    chat_dir = tg_logger.get_chat_log_dir(message.chat.id)

    # Get first message date
    file = open(str(chat_dir) + '/messages.txt', 'r')
    for messages, line in enumerate(file):
        if messages == 0:
            first_msg_date = line[1:line.index(']')]
    file.close()

    # Read number of button clicks
    file = open(str(chat_dir) + '/cb_queries.txt', 'r')
    for clicks, line in enumerate(file):
        pass
    file.close()

    message_text = '*Statistic*\n\nThis chat ID: {chat_id}\nYour ID: {user_id}\nMessages: {messages}\nButton clicks: {clicks}\nFirst message: {first}'.format(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
        messages=messages,
        clicks=clicks,
        first=first_msg_date
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(text=message.lang['button.menu'], callback_data='open.menu'),
        types.InlineKeyboardButton(text='How Did We Get Here?', url='https://github.com/Angron42/sute-schedule-bot')
    )

    msg = {
        'chat_id': message.chat.id,
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'Markdown'
    }

    return msg
