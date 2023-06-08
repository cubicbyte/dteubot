"""
Module for parsing website
"""

import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

from .schemas import Faculty, Chair, Teacher, FullTeacher
from .utils import format_string


PAGE_URL: str = 'https://knute.edu.ua'
REQUEST_TIMEOUT: int = int(os.environ.get('REQUEST_TIMEOUT', '5'))


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
    # 1. Переходимо на сторінку кафедри
    # 2. Переходимо на сторінку викладачів кафедри
    # 3. Парсимо список викладачів
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

            if len(p_els) < 2 or link_el is None or img_el is None:
                continue

            # get full name
            name = teacher_cell.find('a').parent.getText()
            # remove extra spaces and newlines
            name = format_string(name)
            # capitalize each word (IGOR IVANOV -> Igor Ivanov)
            name = ' '.join([s.capitalize() for s in name.split(' ')])

            # Merge all paragraphs into one string
            description = ' '.join([p.getText() for p in p_els[1:]])
            # Remove extra spaces and newlines
            description = format_string(description)
            # Capitalize first letter
            description = description.capitalize()

            teacher = Teacher(
                name=name,
                description=description,    
                photo_link=urljoin(PAGE_URL, img_el['src']),
                page_link=urljoin(PAGE_URL, link_el['href'])
            )

            if teacher.name.count(' ') != 2 or not teacher.description:
                continue

            teachers.append(teacher)

    return teachers


def get_teacher(teacher_page_url: str) -> FullTeacher:
    """Get full teacher info from teacher page"""
    raise NotImplementedError()
