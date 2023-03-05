import telebot.types
import logging
import os
from ..settings import bot, chat_configs, langs
from ..pages import lang_select, settings

logger = logging.getLogger(__name__)

@bot.callback_query_handler(func=lambda call: call.query == 'select.lang')
def handler(call: telebot.types.CallbackQuery):
    logger.debug('Handling callback query')
    lang = call.args['lang']

    if not lang in langs:
        lang = os.getenv('DEFAULT_LANG')

    if lang == call.message.lang_code:
        bot.edit_message_text(**settings.create_message(call.message.lang_code, call.message.config['groupId']), chat_id=call.message.chat.id, message_id=call.message.message_id)
        return

    call.message._config = chat_configs.set_chat_config_field(call.message.chat.id, 'lang', lang)
    bot.edit_message_text(**lang_select.create_message(call.message.lang_code), chat_id=call.message.chat.id, message_id=call.message.message_id)
