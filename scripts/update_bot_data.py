# Updates bot data to the latest version

import os
import json
import logging
import argparse

logging.basicConfig(
    level='INFO',
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

logger = logging.getLogger(__name__)

# Setting cli arguments
parser = argparse.ArgumentParser(description='Update bot data to the latest version')
parser.add_argument('path', type=str, help='Bot data directory path')



def insert_after(key: str, value: any, after_key: str, obj: dict, ignore_existing: bool = True):
    "Inserts a value after a specific key in dict"
    logger.debug('Insert %s: %s after key %s' % (key, value, after_key))
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
    for i in range(len(keys)):
        res[keys[i]] = values[i]
    return res

def update_chat_configs(path: str):
    "Update chat configs (chat data) to the latest version. (outdated)"
    logger.info('Scanning for an outdated chat-configs folder')
    if not os.path.exists(path):
        logger.info('Flder not found.')
        return

    files = os.listdir(path)
    count = len(files)
    logger.info('Updating %s files' % count)
    for i, file in enumerate(files):
        logger.info(f'Progress: {i + 1}/{count}')

        # Read config
        file_path = os.path.join(path, file)
        fp = open(file_path, 'r+')
        conf = json.load(fp)

        # Required to overwrite a file
        fp.seek(0)      # Move cursor to start of the file
        fp.truncate(0)  # Clear file

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

        conf = insert_after('ref', None, 'lang', conf)   # 1.2.0: create "ref" field
        conf = insert_after('admin', False, 'ref', conf) # 1.4.2: create "admin" field

        # 1.5.0: remove structure, faculty and course from config
        if 'schedule' in conf:
            group_id = conf['schedule']['group_id']
            del conf['schedule']
            conf = insert_after('groupId', group_id, 'admin', conf)

        json.dump(conf, fp, indent=4, ensure_ascii=False)
    logger.info('Chat configs updated')

# 2.3.0
def migrate_chat_configs(path: str, user_data_path: str, chat_data_path: str):
    "Migrate the old chat-configs folder to the new format, with the user and chat data separated"
    logger.info('Migrating the old chat-configs folder to the new format')

    if not os.path.exists(path):
        logger.info('Folder not found.')
        return

    os.makedirs(user_data_path, exist_ok=True)
    os.makedirs(chat_data_path, exist_ok=True)

    files = os.listdir(path)
    count = len(files)
    logger.info('Migrating %s files' % count)

    for i, file in enumerate(files):
        logger.info(f'Progress: {i + 1}/{count}')

        # Read config
        file_path = os.path.join(path, file)
        fp = open(file_path)
        conf = json.load(fp)
        fp.close()

        if not file.startswith('-'):
            # All group, supergroup and channel IDs start with "-", which means this thing will only save user data
            user_fp = open(os.path.join(user_data_path, file), 'w')
            user_data = {
                'admin': conf['admin'],
                'ref': conf['ref']}
            json.dump(user_data, user_fp, ensure_ascii=False, indent=4)
            user_fp.close()

        chat_fp = open(os.path.join(chat_data_path, file), 'w')
        chat_data = {
            'lang_code': conf['lang'],
            'group_id': conf['groupId']}
        json.dump(chat_data, chat_fp, ensure_ascii=False, indent=4)
        chat_fp.close()
        os.remove(file_path)

    os.rmdir(path)
    logger.info('Chat configs migrated')

def update_user_data(path: str):
    logger.info('Updating user data')

    files = os.listdir(path)
    count = len(files)
    logger.info('Updating %s files' % count)

    for i, file in enumerate(files):
        logger.info(f'Progress: {i + 1}/{count}')

        # Read config
        file_path = os.path.join(path, file)
        fp = open(file_path, 'r+')
        conf = json.load(fp)

        # Required to overwrite a file
        fp.seek(0)      # Move cursor to start of the file
        fp.truncate(0)  # Clear file

        # 2.3.0: create "_created" and "_updated" fields
        conf = insert_after('_created', 0, 'ref', conf)
        conf = insert_after('_updated', 0, '_created', conf)

        json.dump(conf, fp, ensure_ascii=False, indent=4)
    logger.info('User data updated')

def update_chat_data(path: str):
    logger.info('Updating chat data')

    files = os.listdir(path)
    count = len(files)
    logger.info('Updating %s files' % count)

    for i, file in enumerate(files):
        logger.info(f'Progress: {i + 1}/{count}')

        # Read config
        file_path = os.path.join(path, file)
        fp = open(file_path, 'r+')
        conf = json.load(fp)

        # Required to overwrite a file
        fp.seek(0)      # Move cursor to start of the file
        fp.truncate(0)  # Clear file

        # 2.3.0
        conf = insert_after('cl_notif_15m', False, 'group_id', conf)
        conf = insert_after('cl_notif_1m', False, 'cl_notif_15m', conf)
        conf = insert_after('cl_notif_suggested', False, 'cl_notif_1m', conf)
        conf = insert_after('_accessible', True, 'cl_notif_suggested', conf)
        conf = insert_after('_created', 0, '_accessible', conf)
        conf = insert_after('_updated', 0, '_created', conf)

        json.dump(conf, fp, indent=4, ensure_ascii=False)
    logger.info('Chat data updated')

def update_logs(path: str):
    logger.info('Starting logs parser')

    # 1.6.0: now logs are stored in the single file
    if os.path.exists(os.path.join(path, 'debug')):
        logger.info('logs/debug folder detected, removing')
        os.rmdir(os.path.join(path, 'debug'))

    logger.info('Logs updated')

def update_cache(path: str):
    # TODO
    pass

def update_langs(path: str):
    # TODO
    pass



def main(path: str):
    """Update bot data to the latest version"""
    logger.info('Starting bot data parser')

    chat_configs_path = os.path.join(path, 'chat-configs')
    user_data_path = os.path.join(path, 'user-data')
    chat_data_path = os.path.join(path, 'chat-data')
    logs_path = os.path.join(path, 'logs')
    cache_path = os.path.join(path, 'cache')
    langs_path = os.path.join(path, 'langs')

    update_chat_configs(chat_configs_path)
    migrate_chat_configs(chat_configs_path, user_data_path, chat_data_path)
    update_user_data(user_data_path)
    update_chat_data(chat_data_path)
    update_logs(logs_path)
    update_cache(cache_path)
    update_langs(langs_path)
    logger.info('Bot data updated')

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.path)
