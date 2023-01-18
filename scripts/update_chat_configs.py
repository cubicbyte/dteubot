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
parser = argparse.ArgumentParser(description='Update bot chat configs')
parser.add_argument('path', type=str, help='Chat configs directory path')


def parse_cmd_args():
    "Get command line arguments"

    args = parser.parse_args()
    return vars(args) # Return as dict

def insert_after(key: str, value: any, obj: dict, after_key: str):
    """Inserts a value after a specific key in an object"""

    logger.debug('Insert %s: %s after key %s' % (key, value, after_key))
    keys = list(obj.keys())
    values = list(obj.values())

    # Find the index of the key to be inserted
    i = keys.index(after_key) + 1

    # Insert value
    keys.insert(i, key)
    values.insert(i, value)

    # Write result to new object
    res = {}
    for i in range(len(keys)):
        res[keys[i]] = values[i]

    return res



def main(path: str):
    """Update chat configs to the latest version"""
    logger.info('Starting chat configs parser')

    try:
        logger.info('Reading directory files')
        files = os.listdir(path)
    except FileNotFoundError:
        logger.error('The directory does not exist. Skip update')
        return

    count = len(files)
    logger.info('Converting %s files' % count)

    for i, file in enumerate(files):
        logger.info(f'Converting #{i + 1}/{count}')

        # Read config
        file_path = os.path.join(path, file)
        logger.debug('Opening file %s' % file_path)
        fp = open(file_path, 'r+', encoding='utf-8')
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

        # 1.2.0
        # Create "ref" field
        if not 'ref' in conf:
            conf = insert_after('ref', None, conf, 'lang')

        # 1.4.2
        # Create "admin" field
        if not 'admin' in conf:
            conf = insert_after('admin', False, conf, 'ref')

        # 1.5.0
        # Remove structure, faculty and course from config
        if 'schedule' in conf:
            group_id = conf['schedule']['group_id']
            del conf['schedule']
            conf = insert_after('groupId', group_id, conf, 'admin')

        logger.debug('Writing the updated config to a file')
        json.dump(conf, fp, ensure_ascii=False, indent=4)

    logger.info('Converting done')


if __name__ == '__main__':
    args = parse_cmd_args()
    main(args['path'])
