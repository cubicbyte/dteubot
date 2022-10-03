import os
import json
import logging

from pathlib import Path

logger = logging.getLogger()

def load_langs(dirpath):
    logger.debug('Loading langs from dir %s' % dirpath)

    files = os.listdir(dirpath)
    langs = {}
    
    for filename in files:
        filepath = os.path.join(dirpath, filename)

        logger.debug('Loading lang %s' % filepath)
        
        file = open(filepath, 'r', encoding='utf-8')
        lang = json.load(file)
        file.close()

        lang_name = Path(filepath).stem
        langs[lang_name] = lang
    
    return langs

langs = load_langs('langs')
