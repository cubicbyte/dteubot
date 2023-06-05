import os
import csv
import logging
from difflib import SequenceMatcher
from functools import cache
from lib.teacher_loader.schemas import Teacher

_logger = logging.getLogger(__name__)
csv.field_size_limit(0xfffffff)
teachers_filepath = os.path.join(os.getenv('CACHE_PATH', ''), 'teachers.csv')
cache_exists = os.path.exists(teachers_filepath)

if not cache_exists:
    _logger.warning('Teachers list is not loaded. Run scripts/load_teachers.py to load it.')


@cache
def find_teacher_safe(name: str) -> Teacher | None:
    if not cache_exists:
        return None

    for teacher in teachers:
        ratio = SequenceMatcher(a=teacher.name, b=name).ratio()
        if ratio >= 0.78:
            return teacher

    return None


@cache
def find_teacher_fast(name: str) -> Teacher | None:
    if not cache_exists:
        return None

    for teacher in teachers:
        if teacher.name == name:
            return teacher

    return None


def load_teachers(filepath: str) -> list[Teacher]:
    teachers = []
    file = open(filepath, 'r', encoding='utf-8-sig')
    reader = csv.reader(file, delimiter=';')

    for row in reader:
        teachers.append(Teacher(name=row[0], description=row[1], photo_link=row[2], page_link=row[3]))

    return teachers


if cache_exists:
    teachers = load_teachers(teachers_filepath)
