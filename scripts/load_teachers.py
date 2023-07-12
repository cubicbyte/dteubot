"""
Script for loading teachers to csv file.

Usage:
    python load_teachers.py [filepath?]
"""

# TODO: move most of the code to teacher_loader library

import os
import sys

# Needed to import top-level teacher_loader module
_root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(_root_dir)

import csv

from progress.bar import Bar

from lib.teacher_loader import get_faculties, get_teachers
from lib.teacher_loader.schemas import Teacher


def load_teachers_to_file(filepath: str):
    """Load teachers to csv file"""
    _load_teachers_to_file(filepath, _load_teachers())


def _load_teachers() -> list[Teacher]:
    """Get teachers list from site"""

    print('Loading faculties... ', end='', flush=True)
    faculties = get_faculties()
    print(f'{len(faculties)} faculties loaded')

    # Setup progress bar
    total_chairs = sum(len(faculty.chairs) for faculty in faculties)
    bar = Bar('Loading teachers...', max=total_chairs, suffix='%(index)d/%(max)d [ETA: %(eta)ds]')
    bar.start()

    teachers = []
    for faculty in faculties:
        for chair in faculty.chairs:
            teachers.extend(get_teachers(chair.page_link))
            bar.next()

    bar.finish()
    print('Done!')

    return teachers


def _load_teachers_to_file(filepath: str, teachers: list[Teacher]):
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'description', 'photo_link', 'page_link'])

        for teacher in teachers:
            writer.writerow([teacher.name.lower(), teacher.description,
                             teacher.photo_link, teacher.page_link])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        _filepath = sys.argv[1]
    else:
        _filepath = 'cache/teachers.csv'

    load_teachers_to_file(_filepath)
