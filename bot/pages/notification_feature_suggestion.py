from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['text.yes'], callback_data='set.cl_notif_15m#state=1&suggestion=1'),
        InlineKeyboardButton(text=context._chat_data.get_lang()['text.no'], callback_data='close_page')
    ]]

    return {
        'text': context._chat_data.get_lang()['page.notification_feature_suggestion'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
