from telegram.ext import ContextTypes

def create_message(context: ContextTypes.DEFAULT_TYPE) -> dict:
    return {
        'text': context._chat_data.lang['page.greeting'],
        'parse_mode': 'MarkdownV2'
    }
