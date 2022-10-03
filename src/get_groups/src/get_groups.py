import requests
import os
from bs4 import BeautifulSoup

DEFAULT_SCHEDULE_PAGE_URL = 'https://mia1.knute.edu.ua'

def get_groups(facultyId: str | int, course: str | int, structureId: str | int = None) -> dict:

    req_data = {
        'TimeTableForm[facultyId]': facultyId,
        'TimeTableForm[course]': course
    }

    if structureId is not None:
        req_data['TimeTableForm[structureId]'] = structureId

    schedule_url = os.getenv('SCHEDULE_URL') or DEFAULT_SCHEDULE_PAGE_URL
    page = requests.get(schedule_url + '/time-table/group?type=0', data=req_data)
    soup = BeautifulSoup(page.text, 'html.parser')
    select = soup.find('select', {'id': 'timetableform-groupid'})
    options = select.find_all('option')

    result = {}

    for option in options:
        groupId = option['value']
        groupName = option.contents[0]

        if groupId == '':
            continue
        
        result[groupId] = groupName

    return result

