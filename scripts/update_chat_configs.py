import os
import json
import argparse

# Setting cli arguments
parser = argparse.ArgumentParser(description='Update bot chat configs')
parser.add_argument('path', type=str, help='Chat configs directory path')


def parse_cmd_args():
    'Get command line arguments'

    args = parser.parse_args()
    return vars(args)

def insert_after(key: str, value: any, obj: dict, after_key: str):
    """Inserts a value after a specific key in an object"""

    res = {}
    keys = list(obj.keys())
    values = list(obj.values())
    i = keys.index(after_key) + 1
    
    keys.insert(i, key)
    values.insert(i, value)

    for i in range(len(keys)):
        res[keys[i]] = values[i]

    return res



def main(path: str):
    """Update chat configs to the latest version"""
    files = os.listdir(path)
    count = len(files)

    for i, file in enumerate(files):
        print(f'Converting #{i + 1}/{count}')
        
        # Read config
        fp = open(os.path.join(path, file), 'r+', encoding='utf-8')
        conf = json.load(fp)
        fp.seek(0) # Needed to be able to overwrite the file

        # Create "ref" field
        if not 'ref' in conf:
            conf = insert_after('ref', None, conf, 'lang')

        # Create "admin" field
        if not 'admin' in conf:
            conf = insert_after('admin', False, conf, 'ref')

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


        json.dump(conf, fp, ensure_ascii=False, indent=4)

    print('Done')


if __name__ == '__main__':
    args = parse_cmd_args()
    main(args['path'])
