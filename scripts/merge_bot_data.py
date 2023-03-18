# Merge multiple bot data directories into main one

import os
import time
import json
import shutil
import logging
import datetime
import argparse
from typing import List

logging.basicConfig(
    level='INFO',
    format='%(message)s'
)

_logger = logging.getLogger(__name__)

# Setting cli arguments
_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
Merge multiple bot data directories into main one.
Bot data should be updated to the latest version before merging
by using script update_bot_data.py

Example:
  #This will merge bot data from ~/bot-data-1 and ~/bot-data-2 into ~/main-bot-data
  python merge_bot_data.py -o ~/main-bot-data ~/bot-data-1 ~/bot-data-2 ...''')
_parser.add_argument('-o', '--output', type=str, help='Main bot data directory path')
_parser.add_argument('path', type=str, nargs='*', help='Other bot data directory path to merge')

def merge_user_data(main_path: str, other_path: List[str]):
    _logger.info('Merging ./user-data/')
    _main_path = os.path.join(main_path, 'user-data')
    _other_path = [os.path.join(path, 'user-data') for path in other_path]
    _merge_data(_main_path, _other_path)

def merge_chat_data(main_path: str, other_path: List[str]):
    _logger.info('Merging ./chat-data/')
    _main_path = os.path.join(main_path, 'chat-data')
    _other_path = [os.path.join(path, 'chat-data') for path in other_path]
    _merge_data(_main_path, _other_path)

def merge_cache(main_path: str, other_path: List[str]):
    pass

def merge_logs(main_path: str, other_path: List[str]):
    # debug.log will be ignored
    _logger.info('Merging ./logs/telegram/users/.../latest_update.json')
    _merge_user_latest_updates(main_path, other_path)
    _logger.info('Merging ./logs/telegram/users/.../updates.txt')
    _merge_user_updates(main_path, other_path)
    _logger.info('Merging ./logs/telegram/chats/.../messages.txt')
    _merge_chat_messages(main_path, other_path)
    _logger.info('Merging ./logs/telegram/chats/.../cb_queries.txt')
    _merge_chat_cb_queries(main_path, other_path)

def main(main_path: str, other_path: List[str]):
    """Update bot data to the latest version"""
    merge_user_data(main_path, other_path)
    merge_chat_data(main_path, other_path)
    merge_cache(main_path, other_path)
    merge_logs(main_path, other_path)
    _logger.info(f'Merging finished in {time.process_time():.3f}s')



def _merge_data(main_path: str, other_path: List[str]):
    data_cache = {}

    # Load and merge data, then save to data_cache
    for path in other_path:
        for f in os.listdir(path):
            file = os.path.join(path, f)
            fp = open(file)
            data = json.load(fp)
            fp.close()
            if not f in data_cache:
                mainFile = os.path.join(main_path, f)
                if not os.path.exists(mainFile):
                    data_cache[f] = data
                    continue
                fp = open(mainFile)
                data_cache[f] = json.load(fp)
                fp.close()
            if data['_updated'] > data_cache[f]['_updated']:
                data_cache[f] = data

    for f, data in data_cache.items():
        fp = open(os.path.join(main_path, f), 'w')
        json.dump(data, fp, indent=4, ensure_ascii=False)
        fp.close()

def _merge_chat(fp, cache):
    _cache = cache.copy()
    for line in fp:
        if line == '':
            continue
        timestamp = datetime.datetime.strptime(line[1:20], '%Y-%m-%d %H:%M:%S')
        if len(cache) == 0:
            cache.append([timestamp, line])
            continue
        for i, l in enumerate(_cache):
            if timestamp > l[0]:
                cache.insert(i, [timestamp, line])
                break
            elif timestamp == l[0]:
                break
            cache.append([timestamp, line])

def _get_latest_update_time(fp):
    for line in reversed(fp.readlines()):
        if line.startswith('['):
            return int(datetime.datetime.strptime(line[1:20], '%Y-%m-%d %H:%M:%S').timestamp())
    return int(time.time())

def _merge_user_latest_updates(main_path: str, other_path: List[str]):
    data_cache = {}
    for path in other_path + [main_path]:
        path = os.path.join(path, 'logs', 'telegram', 'users')
        for user_id in os.listdir(path):
            with open(os.path.join(path, user_id, 'updates.txt')) as fp:
                update_time = _get_latest_update_time(fp)
                if not user_id in data_cache or update_time > data_cache[user_id][0]:
                    data_cache[user_id] = [update_time, path]

    for user_id, data in data_cache.items():
        path = os.path.join(main_path, 'logs', 'telegram', 'users')
        if data[1] == path:
            continue
        shutil.copyfile(os.path.join(data[1], user_id, 'latest_update.json'), os.path.join(path, user_id, 'latest_update.json'))

def _merge_user_updates(main_path: str, other_path: List[str]):
    data_cache = {}
    for path in other_path + [main_path]:
        path = os.path.join(path, 'logs', 'telegram', 'users')
        for user_id in os.listdir(path):
            if not user_id in data_cache:
                data_cache[user_id] = []
            with open(os.path.join(path, user_id, 'updates.txt')) as fp:
                _merge_chat(fp, data_cache[user_id])

    for user_id, data in data_cache.items():
        with open(os.path.join(main_path, 'logs', 'telegram', 'users', user_id, 'updates.txt'), 'w') as fp:
            for _, line in reversed(data):
                fp.write(line)

def _merge_chat_messages(main_path: str, other_path: List[str]):
    data_cache = {}
    for path in other_path + [main_path]:
        path = os.path.join(path, 'logs', 'telegram', 'chats')
        for chat_id in os.listdir(path):
            if not chat_id in data_cache:
                data_cache[chat_id] = []
            with open(os.path.join(path, chat_id, 'messages.txt')) as fp:
                _merge_chat(fp, data_cache[chat_id])

    for chat_id, data in data_cache.items():
        with open(os.path.join(main_path, 'logs', 'telegram', 'chats', chat_id, 'messages.txt'), 'w') as fp:
            for _, line in reversed(data):
                fp.write(line)

def _merge_chat_cb_queries(main_path: str, other_path: List[str]):
    data_cache = {}
    for path in other_path + [main_path]:
        path = os.path.join(path, 'logs', 'telegram', 'chats')
        for chat_id in os.listdir(path):
            if not chat_id in data_cache:
                data_cache[chat_id] = []
            with open(os.path.join(path, chat_id, 'cb_queries.txt')) as fp:
                _merge_chat(fp, data_cache[chat_id])

    for chat_id, data in data_cache.items():
        with open(os.path.join(main_path, 'logs', 'telegram', 'chats', chat_id, 'cb_queries.txt'), 'w') as fp:
            for _, line in reversed(data):
                fp.write(line)



if __name__ == '__main__':
    args = _parser.parse_args()
    main(args.output, args.path)
