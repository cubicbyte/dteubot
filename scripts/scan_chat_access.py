#
# Checks each chat to see if the bot has access to it.
# Basically sends a temporary "upload_document" status to all chats, thereby checking if the bot has access to that chat.
#

import os
import json
import logging
import argparse
import requests
from pathlib import Path
from functools import partial
from multiprocessing import Pool

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler())
_logger.setLevel(logging.INFO)

# Setting cli arguments
_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='''
Checks each chat to see if the bot has access to it.''')
_parser.add_argument('-t', '--token', type=str, help='Bot token')
_parser.add_argument('-p', '--path', type=str, help='Bot chat data directory path')



def set_chat_accessibility(file: str, status: bool):
    with open(file, 'r+') as fp:
        data = json.load(fp)
        if '_accessible' not in data:
            raise ValueError('Chat data is not in the latest version. Please update it using update_bot_data.py script')
        data['_accessible'] = status
        fp.seek(0)
        fp.truncate(0)
        json.dump(data, fp, indent=4, ensure_ascii=False)

def scan(file: str, token: str) -> tuple[str, bool]:
    chat_id = Path(file).stem
    _logger.debug(f'Scanning chat {chat_id}')
    url = f'https://api.telegram.org/bot{token}/sendChatAction?chat_id={chat_id}&action=upload_document'
    res = requests.get(url)

    if res.status_code == 200:
        set_chat_accessibility(file, True)
        return file, True

    if res.status_code == 403 or res.status_code == 400:
        set_chat_accessibility(file, False)
        return file, False

def main(token: str, path: str):
    _logger.info('Starting chat accessibility scan')
    files = [os.path.join(path, f) for f in os.listdir(path)]
    flen = len(files)

    i = 0
    with Pool(processes=flen) as pool:
        results = pool.imap_unordered(partial(scan, token=token), files)

        for file, access in results:
            i += 1
            chat_id = Path(file).stem
            indents_1 = ' ' * (len(str(flen)) - len(str(i)))
            indents_2 = ' •' * ((16 - len(chat_id)) // 2)
            if len(chat_id) % 2 != 0:
                indents_2 = ' ' + indents_2
            icon = '✅' if access else '❌'
            _logger.info(f'[{i}/{flen}]{indents_1} {chat_id}{indents_2} {icon}')

    _logger.info('✅ Finished')


if __name__ == '__main__':
    args = _parser.parse_args()
    main(args.token, args.path)
