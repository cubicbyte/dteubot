/*
 * Copyright (c) 2022 Bohdan Marukhnenko
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#/usr/bin/env python3

"""
Script for parsing knute.edu.ua website and loading teachers data

Usage:
    python load_teachers.py

This script will create teachers.csv file with all teachers data
"""

# Check python version
import sys
if sys.version_info < (3, 8):
    print('You are using an outdated version of Python, which can cause errors. Please upgrade to Python 3.8 or newer.')

import os
import csv
from urllib.parse import urljoin
from dataclasses import dataclass

try:
    import regex
    import requests
    from bs4 import BeautifulSoup, Tag
    from progress.bar import Bar
except ImportError:
    print('Please install required libraries: pip install requests~=2.31.0 beautifulsoup4~=4.12.2 regex~=2023.10.3 progress~=1.6')
    exit(1)

PAGE_URL: str = 'https://knute.edu.ua'
REQUEST_TIMEOUT: int = int(os.environ.get('REQUEST_TIMEOUT', '5'))


@dataclass
class Chair:
    """Chair info"""

    name: str
    page_link: str


@dataclass
class Faculty:
    """Faculty info"""

    name: str
    chairs: list[Chair]


@dataclass
class Teacher:
    """Short teacher info"""

    name: str
    description: str
    photo_link: str
    page_link: str


class PageUpdatedException(Exception):
    """Exception when page structure is changed"""


def get_faculties() -> list[Faculty]:
    """Get list of faculties and their chairs"""

    ### Принцип роботи ###
    #
    # На головній сторінці сайту є навігаційне меню, в якому є пункт "Факультети кафедри".
    # При наведенні на цей пункт випадає список факультетів і кафедр, які ми і збираємося парсити.
    #

    req = requests.get(PAGE_URL, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(req.text, 'html.parser')

    # Find navigation bar
    nav_bar = soup.find('ul', class_='nav')
    if nav_bar is None:
        raise PageUpdatedException('Navigation bar not found')

    # Find dropdown menu with chairs
    chairs_dropdown = nav_bar.find('span', class_='short-menu-item', string='Факультети кафедри')
    if chairs_dropdown is None:
        raise PageUpdatedException('Chairs dropdown not found')

    # Find chairs list
    chairs_list = chairs_dropdown.parent.parent.find('ul', class_='dropdown-menu')
    if chairs_list is None:
        raise PageUpdatedException('Chairs list not found')

    # Parse chairs list
    faculties = []
    for element in chairs_list:
        if not isinstance(element, Tag):
            continue

        # If row is faculty
        faculty_el = element.find('span')
        if faculty_el is not None:
            faculty = Faculty(name=faculty_el.string, chairs=[])
            faculties.append(faculty)
            continue

        # If row is chair
        element = element.find('a')
        link = urljoin(PAGE_URL, element['href'])
        faculty.chairs.append(Chair(name=element.string, page_link=link))

    return faculties


def get_teachers(chair_page_url: str) -> list[Teacher]:
    """Get list of teachers from chair page"""

    ### Принцип роботи ###
    #
    # 1. Переходимо на сторінку кафедри (chair_page_url)
    # 2. Знаходимо посилання на сторінку викладачів кафедри
    # 3. Переходимо на сторінку викладачів кафедри
    # 4. Парсимо список викладачів
    #

    # Parse chairs page and get teachers page link
    req = requests.get(chair_page_url, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(req.text, 'html.parser')

    teachers_page_link_el = soup.find('a',
        class_='trix-top-menu-item-hrf',
        string=lambda s: 'склад' in s.lower() or 'виклад' in s.lower())

    if teachers_page_link_el is None:
        raise PageUpdatedException('Teachers page link not found')

    teachers_page_link = urljoin(PAGE_URL, teachers_page_link_el['href'])

    # Parse teachers page to get teachers table
    req = requests.get(teachers_page_link, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(req.text, 'html.parser')
    tables = soup.find_all('tbody')
    if not tables:
        raise PageUpdatedException('Teachers table not found')

    # Parse each teacher
    teachers = []
    for table in tables:
        for teacher_cell in table.find_all('td'):
            link_el = teacher_cell.find('a')
            p_els = teacher_cell.find_all('p')
            img_el = teacher_cell.find('img')

            if len(p_els) == 0 or link_el is None or img_el is None:
                continue

            # Find teacher's name
            for a in teacher_cell.find_all('a'):
                name = a.getText()
                name = format_string(name)  # remove extra spaces and newlines
                if name.count(' ') != 2:
                    name = a.parent.getText()
                    name = format_string(name)

                if name.count(' ') == 2:
                    # Name found
                    break
            else:
                continue

            # capitalize each word (IGOR IVANOV -> Igor Ivanov)
            name = ' '.join([s.capitalize() for s in name.split(' ')])

            # Merge all paragraphs into one string
            description = ' '.join([p.getText() for p in p_els])
            # Remove extra spaces and newlines
            description = format_string(description)
            # Remove teacher's name from description
            if description.lower().startswith(name.lower()):
                description = description[len(name) + 1:] if len(name) + 1 < len(description) else ''
            # Capitalize first letter
            description = description.capitalize()


            teacher = Teacher(
                name=name,
                description=description,
                photo_link=urljoin(PAGE_URL, img_el['src']),
                page_link=urljoin(PAGE_URL, link_el['href'])
            )

            teachers.append(teacher)

    return teachers


def format_string(string: str) -> str:
    """Remove unnecessary characters from string"""
    string = regex.sub(r'[^\S ]', ' ', string)  # remove all whitespace characters except space
    string = regex.sub(' +', ' ', string)       # remove extra spaces
    string = regex.sub(r'\p{C}', '', string)    # remove even more garbage characters, like zero-width space
    return string.strip()


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
        writer.writerow(['name', 'page_link'])

        for teacher in teachers:
            writer.writerow([teacher.name.lower(), teacher.page_link])


if __name__ == '__main__':
    load_teachers_to_file('teachers.csv')
