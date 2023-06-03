import os
import csv
import logging
from difflib import SequenceMatcher
from lib.teacher_loader.schemas import Teacher

_logger = logging.getLogger(__name__)
csv.field_size_limit(0xfffffff)
teachers_filepath = os.path.join(os.getenv('CACHE_PATH', ''), 'teachers.csv')
_file_exists = os.path.exists(teachers_filepath)

if not _file_exists:
    _logger.warning('Teachers list is not loaded. Run scripts/load_teachers.py to load it.')


def find_teacher(full_name: str) -> Teacher | None:
    if not _file_exists:
        return None

    full_name = full_name.lower()
    file = open(teachers_filepath, 'r', encoding='utf-8-sig')
    reader = csv.reader(file, delimiter=';')

    for row in reader:
        name = row[0]
        ratio = SequenceMatcher(a=name, b=full_name).ratio()
        if ratio >= 0.78:
            return Teacher(name=row[0], description=row[1], photo_link=row[2], page_link=row[3])

    return None
