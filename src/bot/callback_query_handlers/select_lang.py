import telebot.types
import logging
import os
from ..settings import bot, chat_configs, langs
from ..messages import create_menu_message

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.lang')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    lang = call.args['lang']

    if not lang in langs:
        lang = os.getenv('DEFAULT_LANG')

    call.message._config = chat_configs.set_chat_config_field(call.message.chat.id, 'lang', lang)
    bot.edit_message_text(**create_menu_message(call.message), message_id=call.message.id)
