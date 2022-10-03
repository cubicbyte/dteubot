import os
import json
import logging

from pathlib import Path
from .get_default_chat_config import get_default_chat_config

logger = logging.getLogger()

class ChatConfigs:
    def __init__(self, configs_dirpath: str):
        logger.debug('Creating ChatConfig instance')

        self.__dirpath = configs_dirpath

        if not os.path.exists(configs_dirpath):
            os.mkdir(configs_dirpath)
        
    def is_chat_config_exists(self, chat_id: int) -> bool:
        config_filepath = os.path.join(self.__dirpath, f'{chat_id}.json')
        
        return os.path.exists(config_filepath)

    def create_chat_config(self, chat_id: int) -> dict[str, any]:
        logger.debug('Creating %s chat config' % chat_id)
        
        config_filepath = os.path.join(self.__dirpath, f'{chat_id}.json')
        config = get_default_chat_config()

        file = open(config_filepath, 'w', encoding='utf-8')
        json.dump(config, file, ensure_ascii=False)
        file.close()

        return config

    def get_chat_config(self, chat_id: int, create: bool = False) -> dict[str, any] | None:
        logger.debug('Getting %s chat config' % chat_id)

        config_filepath = os.path.join(self.__dirpath, f'{chat_id}.json')

        if not self.is_chat_config_exists(chat_id):
            if not create:
                return None
            
            return self.create_chat_config(chat_id)

        file = open(config_filepath, 'r', encoding='utf-8')
        config = json.load(file)
        file.close()

        return config
    
    def set_chat_config(self, chat_id: int, config: dict) -> dict:
        logger.debug('Updating %s chat config' % chat_id)

        config_filepath = os.path.join(self.__dirpath, f'{chat_id}.json')

        file = open(config_filepath, 'w', encoding='utf-8')
        json.dump(config, file, ensure_ascii=False)
        file.close()

        return config

    def set_chat_config_field(self, chat_id: int, field, value) -> bool:
        logger.debug('Updating %s chat config field' % chat_id)

        config = self.get_chat_config(chat_id, True)

        if not field in config:
            return False

        config[field] = value

        self.set_chat_config(chat_id, config)

        return True

chat_configs_path = Path('chat-configs').absolute()
chat_configs = ChatConfigs(chat_configs_path)
