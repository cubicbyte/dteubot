import os
import json
from pathlib import Path

from bot.schemas import Language


def load_langs(dirpath: str) -> dict[str, Language]:
    """Load .json language files from directory"""

    langs = {}

    for file in os.listdir(dirpath):
        filepath = os.path.join(dirpath, file)
        lang = load_lang_file(filepath)
        langs[lang.name] = lang

    return langs


def load_lang_file(filepath: str) -> Language:
    """Load .json language file"""

    lang_name = Path(filepath).stem

    with open(filepath, 'r', encoding='utf-8') as file:
        lang = json.load(file)

    return Language(lang, lang_name)
