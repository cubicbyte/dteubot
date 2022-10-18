import os
import json
import logging

from . import get_default_chat_config

logger = logging.getLogger(__name__)

class ChatConfigs:
    def __init__(self, configs_dirpath: str):
        logger.debug('Creating ChatConfig instance')

        self.__dirpath = configs_dirpath

        if not os.path.exists(configs_dirpath):
            os.mkdir(configs_dirpath)
        
    def is_chat_config_exists(self, chat_id: int) -> bool:
        return os.path.join(self.__dirpath, f'{chat_id}.json')

    def create_chat_config(self, chat_id: int) -> dict[str, any]:
        logger.debug('Creating %s chat config' % chat_id)
        
        config = get_default_chat_config()

        path = os.path.join(self.__dirpath, f'{chat_id}.json')
        fp = open(path, 'w', encoding='utf-8')
        json.dump(config, fp, ensure_ascii=False, indent=4)
        fp.close()

        return config

    def get_chat_config(self, chat_id: int, create = False) -> dict[str, any]:
        logger.debug('Getting %s chat config' % chat_id)

        if create:
            if not self.is_chat_config_exists(chat_id):
                return self.create_chat_config(chat_id)

        path = os.path.join(self.__dirpath, f'{chat_id}.json')
        fp = open(path, 'r', encoding='utf-8')
        config = json.load(fp)
        fp.close()

        return config
    
    def set_chat_config(self, chat_id: int, config: dict[str, any]) -> dict[str, any]:
        logger.debug('Updating %s chat config' % chat_id)

        path = os.path.join(self.__dirpath, f'{chat_id}.json')
        fp = open(path, 'w', encoding='utf-8')
        json.dump(config, fp, ensure_ascii=False, indent=4)
        fp.close()

        return config

    def set_chat_config_field(self, chat_id: int, field: str, value: any, create = False) -> dict[str, any]:
        logger.debug('Updating %s chat config field' % chat_id)

        config = self.get_chat_config(chat_id, create)
        config[field] = value

        return self.set_chat_config(chat_id, config)
