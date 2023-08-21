"""
Updates bot data to the latest version
"""

import os
import time
import json
import logging
import argparse

logging.basicConfig(
    level='INFO',
    format='%(message)s'
)

_logger = logging.getLogger(__name__)

# Setting cli arguments
_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument('path', type=str, help='Bot data directory path')


def insert_after(key: str, value: any, after_key: str, obj: dict, ignore_existing: bool = True):
    """Inserts a value after a specific key in dict"""

    keys = list(obj.keys())
    values = list(obj.values())

    if ignore_existing and key in keys:
        return obj

    # Find the index of the key to be inserted
    i = keys.index(after_key) + 1

    # Insert value
    keys.insert(i, key)
    values.insert(i, value)

    res = {}
    for i, k in enumerate(keys):
        res[keys[i]] = values[i]

    return res


def update_chat_configs(path: str):
    """Update chat configs (chat data) to the latest version. (outdated)"""

    _logger.info('Updating ./chat-configs/ (outdated)')
    path = os.path.join(path, 'chat-configs')

    if not os.path.exists(path):
        _logger.debug('Folder not found')
        return

    files = os.listdir(path)
    count = len(files)
    for i, filename in enumerate(files):
        _logger.debug('[%s/%s] updating %s', i + 1, count, filename)

        # Read config
        with open(os.path.join(path, filename), encoding='utf-8') as file:
            conf = json.load(file)

        # Convert string fields to integers
        if 'schedule' in conf:
            if conf['schedule']['structure_id'] is not None:
                conf['schedule']['structure_id'] = int(conf['schedule']['structure_id'])
            if conf['schedule']['faculty_id'] is not None:
                conf['schedule']['faculty_id'] = int(conf['schedule']['faculty_id'])
            if conf['schedule']['course'] is not None:
                conf['schedule']['course'] = int(conf['schedule']['course'])
            if conf['schedule']['group_id'] is not None:
                conf['schedule']['group_id'] = int(conf['schedule']['group_id'])

        conf = insert_after('ref', None, 'lang', conf)  # 1.2.0: create "ref" field
        conf = insert_after('admin', False, 'ref', conf)  # 1.4.2: create "admin" field

        # 1.5.0: remove structure, faculty and course from config
        if 'schedule' in conf:
            group_id = conf['schedule']['group_id']
            del conf['schedule']
            conf = insert_after('groupId', group_id, 'admin', conf)

        with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
            json.dump(conf, file, indent=2, ensure_ascii=False)


# 2.3.0
def migrate_chat_configs(path: str):
    """
    Migrate the old chat-configs folder to the new format,
    with the user and chat data separated
    """

    _logger.info('Migrating the old ./chat-configs/ folder to the new format')

    path = os.path.join(path, 'chat-configs')
    user_data_path = os.path.join(path, 'user-data')
    chat_data_path = os.path.join(path, 'chat-data')

    if not os.path.exists(path):
        _logger.debug('Folder not found')
        return

    os.makedirs(user_data_path, exist_ok=True)
    os.makedirs(chat_data_path, exist_ok=True)

    files = os.listdir(path)
    count = len(files)

    for i, filename in enumerate(files):
        _logger.debug('[%s/%s] migrating %s', i + 1, count, filename)

        # Read config
        filepath = os.path.join(path, filename)
        with open(filepath, encoding='utf-8') as file:
            conf = json.load(file)

        if not filename.startswith('-'):
            # All group, supergroup and channel IDs start with "-",
            # which means this thing will only save user data
            user_data = {
                'admin': conf['admin'],
                'ref': conf['ref']
            }

            with open(os.path.join(user_data_path, filename), 'w', encoding='utf-8') as file:
                json.dump(user_data, file, ensure_ascii=False, indent=2)

        chat_data = {
            'lang_code': conf['lang'],
            'group_id': conf['groupId']
        }

        with open(os.path.join(chat_data_path, filename), 'w', encoding='utf-8') as file:
            json.dump(chat_data, file, ensure_ascii=False, indent=2)

        os.remove(filepath)

    os.rmdir(path)


def update_user_data(path: str):
    """Update user data to the latest version"""

    _logger.info('Updating ./user-data/')

    path = os.path.join(path, 'user-data')
    files = os.listdir(path)
    count = len(files)

    for i, filename in enumerate(files):
        _logger.debug('[%s/%s] updating %s', i + 1, count, filename)

        # Read config
        with open(os.path.join(path, filename), encoding='utf-8') as file:
            conf = json.load(file)

        # 2.3.0: create "_created" and "_updated" fields
        conf = insert_after('_created', 0, 'ref', conf)
        conf = insert_after('_updated', 0, '_created', conf)

        with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
            json.dump(conf, file, ensure_ascii=False, indent=2)


def update_chat_data(path: str):
    """Update chat data to the latest version"""

    _logger.info('Updating ./chat-data/')

    path = os.path.join(path, 'chat-data')
    files = os.listdir(path)
    count = len(files)

    for i, filename in enumerate(files):
        _logger.debug('[%s/%s] updating %s', i + 1, count, filename)

        # Read config
        with open(os.path.join(path, filename), encoding='utf-8') as file:
            conf = json.load(file)

        # Remove cl_notif_suggested
        conf.pop('cl_notif_suggested', None)

        conf = insert_after('cl_notif_15m', False, 'group_id', conf)
        conf = insert_after('cl_notif_1m', False, 'cl_notif_15m', conf)
        conf = insert_after('seen_settings', True, 'cl_notif_1m', conf)
        conf = insert_after('_accessible', True, 'seen_settings', conf)
        conf = insert_after('_created', 0, '_accessible', conf)
        conf = insert_after('_updated', 0, '_created', conf)

        with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:
            json.dump(conf, file, indent=2, ensure_ascii=False)


def update_logs(path: str):
    """Update logs to the latest version"""

    _logger.info('Updating ./logs/')
    path = os.path.join(path, 'logs')

    # 1.6.0: now logs are stored in the single file
    if os.path.exists(os.path.join(path, 'debug')):
        _logger.debug('./logs/debug/ folder detected. Removing')
        os.rmdir(os.path.join(path, 'debug'))


def update_cache(path: str):
    # pylint: disable=unused-argument
    """Update cache to the latest version"""


def update_langs(path: str):
    # pylint: disable=unused-argument
    """Update langs to the latest version"""


def main(path: str):
    """Update bot data to the latest version"""

    update_chat_configs(path)
    migrate_chat_configs(path)
    update_user_data(path)
    update_chat_data(path)
    update_logs(path)
    update_cache(path)
    update_langs(path)

    _logger.info('Bot data updated in %ss', round(time.process_time(), 3))


if __name__ == '__main__':
    args = _parser.parse_args()
    main(args.path)
