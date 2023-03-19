from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    buttons = [
        [InlineKeyboardButton(text=context._chat_data.get_lang()['button.admin.clear_expired_cache'], callback_data='admin.clear_expired_cache')],
        [InlineKeyboardButton(text=context._chat_data.get_lang()['button.admin.clear_all_cache'], callback_data='admin.clear_all_cache')],
        [InlineKeyboardButton(text=context._chat_data.get_lang()['button.admin.get_logs'], callback_data='admin.get_logs')],
        [InlineKeyboardButton(text=context._chat_data.get_lang()['button.admin.clear_logs'], callback_data='admin.clear_logs')],
        [InlineKeyboardButton(text=context._chat_data.get_lang()['button.back'], callback_data='open.menu')]
    ]

    return {
        'text': context._chat_data.get_lang()['page.admin_panel'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
