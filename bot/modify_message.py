import os
import telebot.types
from .settings import chat_configs, langs
from .parse_callback_query import parse_callback_query



def update_config(self, create = False):
    self._config = chat_configs.get_chat_config(self._config_id, create)


@property
def config_created(self):
    return chat_configs.is_chat_config_exists(self._config_id)

@property
def config(self):
    if self._config is None:
        self.update_config(True)

    return self._config

@property
def lang_code(self):
    lang_code = self.config['lang']

    if lang_code is None:
        if hasattr(self, 'from_user'):
            lang_code = self.from_user.language_code
        else:
            lang_code = self.message.from_user.language_code

        if not lang_code in langs:
            lang_code = os.getenv('DEFAULT_LANG')

        self._config['lang'] = chat_configs.set_chat_config_field(self._config_id, 'lang', lang_code)

    return lang_code

@lang_code.setter
def lang_code(self, lang_code: str):
    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')
    
    self._config = chat_configs.set_chat_config_field(self._config_id, 'lang', lang_code, True)

@property
def lang(self):
    return langs[self.lang_code]

@property
def args_case(self):
    if self._args_case is None:
        self._args_case = self.text.split(' ')[1:]

    return self._args_case

@property
def message_args(self):
    if self._args is None:
        self._args = list(arg.lower() for arg in self.args_case)

    return self._args

@property
def call_query(self):
    if self._query is None:
        res = parse_callback_query(self.data)
        self._query = res['query']
        self._args = res['args']

    return self._query

@property
def call_args(self):
    if self._args is None:
        res = parse_callback_query(self.data)
        self._query = res['query']
        self._args = res['args']

    return self._args



class CallbackQueryChat:
    def __init__(self, call: telebot.types.CallbackQuery):
        self._call = call
        self._config_id = call.message.chat.id
        self._config = None

class CallbackQueryUser:
    def __init__(self, call: telebot.types.CallbackQuery):
        self._call = call
        self._config_id = call.from_user.id
        self._config = None

def modify_message(message: telebot.types.Message):
    message._config_id = message.chat.id
    message._config = None
    message._args = None
    message._args_case = None

def modify_callback_query(call: telebot.types.CallbackQuery):
    modify_message(call.message)
    call._query = None
    call._args = None
    call.chat = CallbackQueryChat(call)
    call.user = CallbackQueryUser(call)

CallbackQueryChat.update_config = update_config
CallbackQueryUser.update_config = update_config
CallbackQueryChat.config = config
CallbackQueryUser.config = config
CallbackQueryChat.lang_code = lang_code
CallbackQueryUser.lang_code = lang_code
CallbackQueryChat.lang = lang
CallbackQueryUser.lang = lang

telebot.types.Message.update_config = update_config
telebot.types.Message.config_created = config_created
telebot.types.Message.config = config
telebot.types.Message.lang_code = lang_code
telebot.types.Message.lang = lang
telebot.types.Message.args_case = args_case
telebot.types.Message.args = message_args

telebot.types.CallbackQuery.query = call_query
telebot.types.CallbackQuery.args = call_args
