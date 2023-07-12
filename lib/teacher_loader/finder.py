# pylint: disable=invalid-name

"""
This module contains functions for finding teachers on the university website.
Used to show users teacher profile links.
"""

import csv
from difflib import SequenceMatcher
from functools import cache

from .schemas import Teacher

csv.field_size_limit(0xfffffff)


class TeacherFinder:
    """
    Class for finding teachers on the university website

    Example:
    --------
    >>> finder = TeacherFinder('teachers.csv')
    >>> finder.find_safe('Семідоцька Вікторія Анатоліївна')
    Teacher(name='Семідоцька Вікторія Анатоліївна', description=..., photo_link=..., page_link=...)
    """

    def __init__(self, filepath: str):
        """
        :param filepath: Path to CSV file with teachers
        """
        self.filepath = filepath
        self._teachers = []
        self.load_teachers()

    @cache
    def find_safe(self, name: str) -> Teacher | None:
        """Find teacher in the database by percentage of similarity"""

        name = name.lower()

        for teacher in self._teachers:
            ratio = SequenceMatcher(a=name, b=teacher.name).ratio()
            if ratio >= 0.78:
                return teacher

        return None

    @cache
    def find_fast(self, name: str) -> Teacher | None:
        """Find teacher in the database by exact match"""

        name = name.lower()

        for teacher in self._teachers:
            if teacher.name == name:
                return teacher

        return None

    def load_teachers(self):
        """Load teachers from CSV file"""

        with open(self.filepath, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')

            for row in reader:
                self._teachers.append(Teacher(
                    name=row[0], description=row[1],
                    photo_link=row[2], page_link=row[3]))
