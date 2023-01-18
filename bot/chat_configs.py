import os
import json
import logging
from .default_chat_config import DEFAULT_CHAT_CONFIG
from .utils.fs import open_file, exists

logger = logging.getLogger(__name__)



class ChatConfigs:
    """Chat config database that stores data in files"""
    def __init__(self, configs_dirpath: str):
        logger.info('Creating ChatConfig instance')

        self.__dirpath = configs_dirpath

        if not os.path.exists(configs_dirpath):
            os.mkdir(configs_dirpath)

    def _get_chat_config_path(self, chat_id: int) -> str:
        """Returns chat config file path"""
        return os.path.join(self.__dirpath, f'{chat_id}.json')

    def is_chat_config_exists(self, chat_id: int) -> bool:
        """Checks if chat config exists"""
        return exists(self._get_chat_config_path(chat_id))


    def create_chat_config(self, chat_id: int) -> dict[str, any]:
        """Creates new chat config"""
        logger.info('Creating %s chat config' % chat_id)

        config = DEFAULT_CHAT_CONFIG.copy()
        path = os.path.join(self.__dirpath, f'{chat_id}.json')
        fp = open_file(path, 'w', encoding='utf-8')
        logger.debug('Writing a newly created config to a file')
        json.dump(config, fp, ensure_ascii=False, indent=4)
        fp.close()

        return config

    def get_chat_config(self, chat_id: int, create = False) -> dict[str, any]:
        """Returns chat config"""
        logger.debug('Getting %s chat config' % chat_id)

        if create:
            if not self.is_chat_config_exists(chat_id):
                return self.create_chat_config(chat_id)

        path = os.path.join(self.__dirpath, f'{chat_id}.json')
        fp = open_file(path, 'r', encoding='utf-8')
        logger.debug('Reading config from a file')
        config = json.load(fp)
        fp.close()

        return config

    def set_chat_config(self, chat_id: int, config: dict[str, any]) -> dict[str, any]:
        """Updates chat config"""
        logger.debug('Updating %s chat config' % chat_id)

        path = os.path.join(self.__dirpath, f'{chat_id}.json')
        fp = open_file(path, 'w', encoding='utf-8')
        logger.debug('Writing config to file')
        json.dump(config, fp, ensure_ascii=False, indent=4)
        fp.close()

        return config

    def set_chat_config_field(self, chat_id: int, field: str, value: any, create = False) -> dict[str, any]:
        """Updates given chat config field"""
        logger.debug('Updating %s chat config field "%s" with value "%s"' % (chat_id, field, value))

        config = self.get_chat_config(chat_id, create)
        config[field] = value

        return self.set_chat_config(chat_id, config)
