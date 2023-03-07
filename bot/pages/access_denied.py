from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    lang_code = context.chat_data.get('lang')
    message_text = context.bot_data['langs'][lang_code]['alert.no_permissions']
    markup = InlineKeyboardMarkup(
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.menu'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
