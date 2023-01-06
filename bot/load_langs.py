import os
import sys
import json
import logging
from pathlib import Path
from .utils.fs import open_file

logger = logging.getLogger(__name__)



def load_langs(dirpath: str) -> dict[str, dict[str, str]]:
    "Load .json language files from directory"

    dirpath = os.path.join(sys.path[0], dirpath)
    logger.info('Loading langs from dir %s' % dirpath)

    files = os.listdir(dirpath)
    logger.info('Found %s files' % len(files))

    langs = {}
    for filename in files:
        filepath = os.path.join(dirpath, filename)
        lang_name = Path(filename).stem # File name without .json
        logger.info('Loading %s lang' % lang_name)

        # Load lang
        fp = open_file(filepath, 'r', encoding='utf-8')
        logger.debug('Reading json content of a file')
        lang = json.load(fp)
        fp.close()

        langs[lang_name] = lang

    return langs
