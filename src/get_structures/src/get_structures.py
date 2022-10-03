import requests
import os
from bs4 import BeautifulSoup

DEFAULT_SCHEDULE_PAGE_URL = 'https://mia1.knute.edu.ua'

def get_structures() -> dict:

    schedule_url = os.getenv('SCHEDULE_URL') or DEFAULT_SCHEDULE_PAGE_URL
    page = requests.get(schedule_url + '/time-table/group?type=0')
    soup = BeautifulSoup(page.text, 'html.parser')
    select = soup.find('select', {'id': 'timetableform-structureid'})

    if select is None:
        return {}

    options = select.find_all('option')

    result = {}

    for option in options:
        facultyId = option['value']
        facultyName = option.contents[0]

        if facultyId == '':
            continue
        
        result[facultyId] = facultyName

    return result

