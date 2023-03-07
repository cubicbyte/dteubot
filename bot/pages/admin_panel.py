from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    lang_code = context.chat_data.get('lang')
    message_text = context.bot_data['langs'][lang_code]['page.admin_panel']

    markup = InlineKeyboardMarkup(
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.admin.clear_expired_cache'], callback_data='admin.clear_expired_cache'),
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.admin.clear_all_cache'], callback_data='admin.clear_all_cache'),
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.admin.get_logs'], callback_data='admin.get_logs'),
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.admin.clear_logs'], callback_data='admin.clear_logs'),
        InlineKeyboardButton(text=context.bot_data['langs'][lang_code]['button.back'], callback_data='open.menu')
    )

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
