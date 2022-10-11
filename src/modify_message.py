import os
import telebot.types

from .load_langs import langs
from .chat_configs import chat_configs



def modify_message(message: telebot.types.Message = None, call: telebot.types.CallbackQuery = None):
    if message is None:
        message = call.message

    message._call = call
    message._config = None
    message._args = None
    message._args_case = None



def update_config(self, create = False):
    self._config = chat_configs.get_chat_config(self.chat.id, create)


@property
def config_created(self):
    return chat_configs.is_chat_config_exists(self.chat.id)

@property
def config(self):
    if self._config is None:
        self.update_config(True)

    return self._config

@config.setter
def config(self, config: dict[str, any]):
    chat_configs.set_chat_config(self.chat.id, config)

@property
def lang_code(self):
    lang_code = self.config['lang']

    if lang_code is None:
        if self._call is None:
            lang_code = self.from_user.language_code
        else:
            lang_code = self._call.from_user.language_code

        if not lang_code in langs:
            lang_code = os.getenv('DEFAULT_LANG')

        
        self._config['lang'] = chat_configs.set_chat_config_field(self.chat.id, 'lang', lang_code)

    return lang_code

@lang_code.setter
def lang_code(self, lang_code: str):
    if not lang_code in langs:
        lang_code = os.getenv('DEFAULT_LANG')
    
    self._config = chat_configs.set_chat_config_field(self.chat.id, 'lang', lang_code, True)

@property
def lang(self):
    return langs[self.lang_code]

@property
def args_case(self):
    if self._args_case is None:
        self._args_case = self.text.split(' ')[1:]

    return self._args_case

@property
def args(self):
    if self._args is None:
        self._args = list(arg.lower() for arg in self.args_case)

    return self._args


telebot.types.Message.update_config = update_config
telebot.types.Message.config_created = config_created
telebot.types.Message.config = config
telebot.types.Message.lang_code = lang_code
telebot.types.Message.lang = lang
telebot.types.Message.args_case = args_case
telebot.types.Message.args = args
