import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag
from .schemas import Faculty, Chair, Teacher, FullTeacher
from .utils import format_string


page_url = 'https://knute.edu.ua'


class PageUpdatedException(Exception):
    """Exception when page structure is changed"""
    pass


def get_faculties() -> list[Faculty]:
    """Get list of faculties and their chairs"""

    ### Принцип роботи ###
    #
    # На головній сторінці сайту є навігаційне меню, в якому є пункт "Факультети кафедри".
    # При наведенні на цей пункт випадає список факультетів і кафедр, які ми і збираємося парсити.
    #

    req = requests.get(page_url)
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
    for el in chairs_list:
        if type(el) is not Tag:
            continue

        # If row is faculty
        faculty_el = el.find('span')
        if faculty_el is not None:
            faculty = Faculty(name=faculty_el.string, chairs=[])
            faculties.append(faculty)
            continue

        # If row is chair
        chair_el = el.find('a')
        link = urljoin(page_url, chair_el['href'])
        faculty.chairs.append(Chair(name=chair_el.string, page_link=link))

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
    req = requests.get(chair_page_url)
    soup = BeautifulSoup(req.text, 'html.parser')

    teachers_page_link_el = soup.find('a',
        class_='trix-top-menu-item-hrf',
        string=lambda s: 'склад' in s.lower() or 'виклад' in s.lower())

    if teachers_page_link_el is None:
        raise PageUpdatedException('Teachers page link not found')

    teachers_page_link = urljoin(page_url, teachers_page_link_el['href'])

    # Parse teachers page
    req = requests.get(teachers_page_link)
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

            name = teacher_cell.find('a').parent.getText()              # get full name
            name = format_string(name)                                  # remove extra spaces and newlines
            name = ' '.join([s.capitalize() for s in name.split(' ')])  # capitalize each word (IGOR IVANOV -> Igor Ivanov)

            teacher = Teacher(
                name=name,
                description=format_string(p_els[-1].getText()).capitalize(),
                photo_link=urljoin(page_url, img_el['src']),
                page_link=urljoin(page_url, link_el['href'])
            )

            if teacher.name.count(' ') != 2 or not teacher.description:
                continue

            teachers.append(teacher)

    return teachers


def get_teacher(teacher_page_url: str) -> FullTeacher:
    raise NotImplementedError()
