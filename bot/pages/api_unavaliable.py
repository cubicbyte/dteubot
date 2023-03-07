from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes) -> dict:
    message_text = context.bot_data['langs'][lang_code]['page.api_unavaliable']
    markup = InlineKeyboardMarkup(
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.menu'], callback_data='open.menu'),
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.write_me'], url='https://t.me/cubicbyte')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
