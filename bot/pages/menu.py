from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    buttons = [[
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.schedule'], callback_data='open.schedule.today')
    ], [
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.settings'], callback_data='open.settings'),
        InlineKeyboardButton(text=context._chat_data.get_lang()['button.more'], callback_data='open.more')
    ]]

    # If user is admin, then add control panel button
    if context._user_data.admin:
        buttons.append([
            InlineKeyboardButton(text=context._chat_data.get_lang()['button.admin.panel'], callback_data='admin.open_panel')
        ])

    return {
        'text': context._chat_data.get_lang()['page.menu'],
        'reply_markup': InlineKeyboardMarkup(buttons),
        'parse_mode': 'MarkdownV2'
    }
