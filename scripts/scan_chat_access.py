"""
Checks each chat to see if the bot has access to it.
Basically sends a temporary "upload_document" status to all chats,
thereby checking if the bot has access to that chat.
"""

import os
import json
import logging
import argparse
from pathlib import Path
from functools import partial
from multiprocessing import Pool

import requests

REQUEST_TIMEOUT: int = int(os.environ.get('REQUEST_TIMEOUT', '5'))


_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler())
_logger.setLevel(logging.INFO)

# Setting cli arguments
_parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
_parser.add_argument('-t', '--token', type=str, help='Bot token')
_parser.add_argument('-p', '--path', type=str, help='Bot chat data directory path')


def set_chat_accessibility(filepath: str, status: bool):
    """Set chat accessibility status"""

    with open(filepath, 'r+', encoding='utf-8') as file:
        data = json.load(file)

        if '_accessible' not in data:
            raise ValueError('Chat data is not in the latest version. \
                              Please update it using update_bot_data.py script')

        data['_accessible'] = status
        file.seek(0)
        file.truncate(0)
        json.dump(data, file, indent=2, ensure_ascii=False)


def scan(file: str, token: str) -> tuple[str, bool]:
    """Scan chat accessibility"""

    chat_id = Path(file).stem
    _logger.debug('Scanning chat %s', chat_id)
    url = f'https://api.telegram.org/bot{token}/sendChatAction?\
        chat_id={chat_id}&\
        action=upload_document'
    res = requests.get(url, timeout=REQUEST_TIMEOUT)

    if res.status_code == 200:
        set_chat_accessibility(file, True)
        return file, True

    set_chat_accessibility(file, False)
    return file, False


def main(token: str, path: str):
    """Main function"""

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
            _logger.info('[%s/%s]%s %s%s %s', i, flen, indents_1, chat_id, indents_2, icon)

    _logger.info('✅ Finished')


if __name__ == '__main__':
    args = _parser.parse_args()
    main(args.token, args.path)
