#
# Checks each chat to see if the bot has access to it.
# Basically sends a temporary "upload_document" status to all chats, thereby checking if the bot has access to that chat.
#

import os
import json
import asyncio
import logging
import argparse
from telegram import Bot
from telegram.error import BadRequest, Forbidden

class MStreamHandler(logging.StreamHandler):
    # https://stackoverflow.com/a/65235302/19633174
    """Handler that controls the writing of the newline character"""
    special_code = '[!n]'

    def emit(self, record) -> None:
        if self.special_code in record.msg:
            record.msg = record.msg.replace(self.special_code, '')
            self.terminator = ''
        else:
            self.terminator = '\n'

        return super().emit(record)

_logger = logging.getLogger(__name__)
_logger.addHandler(MStreamHandler())
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

async def main(token: str, path: str):
    _logger.info('Starting chat access scan')
    bot = Bot(token)
    for f in os.listdir(path):
        file = os.path.join(path, f)
        chat_id = f.split('.')[0]
        _logger.info(f'Scanning chat {chat_id}[!n]')
        try:
            await bot.send_chat_action(chat_id, 'upload_document')
        except BadRequest as e:
            if not (e.message.startswith('Chat not found') or
                    e.message.startswith('Peer_id_invalid')):
                raise e
            access = False
        except Forbidden:
            access = False
        else:
            access = True
        finally:
            set_chat_accessibility(file, access)
            indents = ' •' * ((16 - len(chat_id)) // 2)
            if len(chat_id) % 2 != 0:
                indents = ' ' + indents
            icon = '✅' if access else '❌'
            _logger.info(f'{indents} {icon}')


if __name__ == '__main__':
    args = _parser.parse_args()
    asyncio.run(main(args.token, args.path))
