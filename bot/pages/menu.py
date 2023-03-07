from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    message_text = context.bot_data['langs'][context.chat_data['lang']]['page.menu']

    buttons = [
        [
            InlineKeyboardButton(text=context.bot_data['langs'][context.chat_data['lang']]['button.schedule'], callback_data='open.schedule.today')
        ], [
            InlineKeyboardButton(text=context.bot_data['langs'][context.chat_data['lang']]['button.settings'], callback_data='open.settings'),
            InlineKeyboardButton(text=context.bot_data['langs'][context.chat_data['lang']]['button.more'], callback_data='open.more')
        ]
    ]

    # If user is admin, then add control panel button
    if context.user_data['admin'] is True:
        buttons.append([
            InlineKeyboardButton(text=context.bot_data['langs'][context.chat_data['lang']]['button.admin.panel'], callback_data='admin.open_panel')
        ])

    markup = InlineKeyboardMarkup(buttons)

    msg = {
        'text': message_text,
        'reply_markup': markup,
        'parse_mode': 'MarkdownV2'
    }

    return msg
