import logging
import os

logger = logging.getLogger(__name__)

def mkdir(path: str):
    "Creates a directory"
    logger.info('Creating dir %s' % path)
    os.mkdir(path)

def mkdir_safe(path: str):
    "Creates a directory if it doesn't exist"
    if os.path.exists(path):
        logger.info('%s dir is already exists. Skipping creation' % path)
    else:
        mkdir(path)

def create_file(path: str):
    "Creates a file"
    logger.info('Creating file %s' % path)
    open(path, 'w').close()

def open_file(path: str, *args, **kwargs):
    "Opens a file"
    logger.debug('Opening file %s' % path)
    return open(path, *args, **kwargs)

def exists(path: str):
    "Returns whether a file/directory exists"
    logger.debug('Accessing %s' % path)
    return os.path.exists(path)
