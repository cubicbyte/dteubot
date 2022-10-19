import os
import json

def main(path: str):
    """Update chat configs to the latest version"""
    files = os.listdir(path)
    count = len(files)

    for i, file in enumerate(files):
        print(f'Converting #{i + 1}/{count}')
        
        fp = open(os.path.join(path, file), 'r+', encoding='utf-8')
        conf = json.load(fp)
        fp.seek(0)

        if 'schedule' in conf:
            # Convert string fields to integers
            if conf['schedule']['structure_id'] is not None:
                conf['schedule']['structure_id'] = int(conf['schedule']['structure_id'])

            if conf['schedule']['faculty_id'] is not None:
                conf['schedule']['faculty_id'] = int(conf['schedule']['faculty_id'])

            if conf['schedule']['course'] is not None:
                conf['schedule']['course'] = int(conf['schedule']['course'])

            if conf['schedule']['group_id'] is not None:
                conf['schedule']['group_id'] = int(conf['schedule']['group_id'])

        if not 'ref' in conf:
            # Insert "ref" field after "lang" field
            n_conf = {}
            keys = list(conf.keys())
            values = list(conf.values())
            i = keys.index('lang') + 1
            
            keys.insert(i, 'ref')
            values.insert(i, None)

            for i in range(len(keys)):
                n_conf[keys[i]] = values[i]

            conf = n_conf

        json.dump(conf, fp, ensure_ascii=False, indent=4)

    print('Done')

if __name__ == '__main__':
    path = input('Enter chat configs directory path >> ')
    main(path)
