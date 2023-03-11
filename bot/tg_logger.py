import os
import logging
import json
from datetime import datetime
from telegram import Update


logger = logging.getLogger(__name__)



class TelegramLogger:
    """Logger to log messages/button clicks"""
    def __init__(self, dirpath):
        logger.debug('Creating TelegramLogger instance')

        self.__dirpath = dirpath
        self.__init_dirs()

    def get_chat_log_dir(self, chat_id: int) -> str:
        """Returns chat log dirpath"""
        return os.path.join(self.__dirpath, 'chats', str(chat_id))

    def get_user_log_dir(self, user_id: int) -> str:
        """Returns user log dirpath"""
        return os.path.join(self.__dirpath, 'users', str(user_id))

    def __init_dirs(self):
        logger.info('Initializing TelegramLogger dirs')
        os.makedirs(self.__dirpath, exist_ok=True)
        os.makedirs(os.path.join(self.__dirpath, 'chats'), exist_ok=True)
        os.makedirs(os.path.join(self.__dirpath, 'users'), exist_ok=True)

    def __chat_log_initialized(self, chat_id: int) -> bool:
        return os.path.exists(self.get_chat_log_dir(chat_id))

    def __user_log_initialized(self, user_id: int) -> bool:
        return os.path.exists(self.get_user_log_dir(user_id))

    def __init_chat_log(self, chat_id: int):
        logger.info('Initializing %s chat log' % chat_id)
        dirpath = self.get_chat_log_dir(chat_id)
        os.mkdir(dirpath)
        open(os.path.join(dirpath, 'messages.txt'), 'w').close()
        open(os.path.join(dirpath, 'cb_queries.txt'), 'w').close()

    def __init_user_log(self, user_id: int):
        logger.info('Initializing %s user log' % user_id)
        dirpath = self.get_user_log_dir(user_id)
        os.mkdir(dirpath)
        open(os.path.join(dirpath, 'updates.txt'), 'w').close()
        fp = open(os.path.join(dirpath, 'latest_update.json'), 'w')
        fp.write('{}')
        fp.close()

    def __handle_user_update(self, update: Update):
        "Logs user profile updates"

        logger.info('Handling %s user update' % update.effective_user.id)
        user_dir = self.get_user_log_dir(update.effective_user.id)
        user_dict = update.effective_user.to_dict()
        latest_update_path = os.path.join(user_dir, 'latest_update.json')
        updates_path = os.path.join(user_dir, 'updates.txt')

        # Reading an old user update to compare with the new one
        fp = open(latest_update_path, 'r', encoding='utf8')
        logger.debug('Reading user update json file')
        latest_update = json.load(fp)
        fp.close()

        # Checks if any user fields have been updated
        upd = {}
        for field in user_dict:
            if not field in latest_update or user_dict[field] != latest_update[field]:
                upd[field] = user_dict[field]
        for field in latest_update:
            if not field in user_dict:
                upd[field] = None

        # If the user profile is updated, write the new changes
        if upd:
            # Record the full update
            logger.info('User profile updated, recording update...')
            fp = open(latest_update_path, 'w', encoding='utf8')
            logger.debug('Recording the full user profile')
            json.dump(user_dict, fp, ensure_ascii=False, indent=4)
            fp.close()

            # Record only updated fields
            fp = open(updates_path, 'a', encoding='utf8')
            logger.debug('Recording only updated fields...')
            fp.write('[{time}] {update}'.format(
                time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                update=json.dumps(upd, ensure_ascii=False)
            ).replace('\n', '\\n') + '\n')
            fp.close()
        else:
            logger.info('No user profile updates detected')

    def __handle_message(self, update: Update):
        "Logs messages, usually commands"

        logger.info('Handling message')
        chat_dir = os.path.join(self.__dirpath, 'chats', str(update.effective_chat.id))

        # Escape line breaks from message
        if update.effective_message.text is not None:
            msg_text = update.effective_message.text.replace('\n', '\\n')
        else:
            msg_text = None

        # Saving a message to the logs
        fp = open(os.path.join(chat_dir, 'messages.txt'), 'a', encoding='utf8')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {text}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message_id=update.effective_message.id,
            text=msg_text
        ))
        fp.close()

    def __handle_callback_query(self, update: Update):
        "Logs callback queries"

        logger.info('Handling callback query %s' % update.callback_query.data)
        chat_dir = os.path.join(self.__dirpath, 'chats', str(update.effective_chat.id))

        # Saving a callback query to the logs
        fp = open(os.path.join(chat_dir, 'cb_queries.txt'), 'a')
        fp.write('[{time}] {chat_id}/{user_id}/{message_id}: {data}\n'.format(
            time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            chat_id=update.effective_chat.id,
            user_id=update.effective_user.id,
            message_id=update.effective_message.id,
            data=update.callback_query.data
        ))
        fp.close()



    async def message_handler(self, update: Update, ctx):
        logger.info('Handling message from chat %s' % update.effective_chat.id)

        if not self.__chat_log_initialized(update.effective_chat.id):
            self.__init_chat_log(update.effective_chat.id)

        if not self.__user_log_initialized(update.effective_user.id):
            self.__init_user_log(update.effective_user.id)

        self.__handle_message(update)
        self.__handle_user_update(update)

    async def callback_query_handler(self, update: Update, ctx):
        logger.info('Handling callback query from chat %s' % update.effective_chat.id)

        if not self.__chat_log_initialized(update.effective_chat.id):
            self.__init_chat_log(update.effective_chat.id)

        if not self.__user_log_initialized(update.effective_user.id):
            self.__init_user_log(update.effective_user.id)

        self.__handle_callback_query(update)
        self.__handle_user_update(update)
