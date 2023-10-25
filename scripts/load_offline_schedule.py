#!/usr/bin/env python3
# Copyright (c) 2022 Bohdan Marukhnenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Script for loading schedule for all groups to work offline.

This script will load data into api cache.
If cache file is not specified, it will search api.sqlite cache file in the following directories:
    - ./
    - ./cache/
"""

import os
import sys
import time
import json
import urllib3
import sqlite3
import argparse
from typing import List, Dict, Optional, Generator
from datetime import date, timedelta

API_URL = os.getenv('API_URL', 'https://mia.mobil.knute.edu.ua')
DB_FLUSH_INTERVAL = 100  # How many groups to process before flushing data to cache file

# Check python version
if sys.version_info < (3, 8):
    print('You are using an outdated version of Python, which can cause errors. Please upgrade to Python 3.8 or newer.')


def main(cache_file: str, date_start: str, date_end: str):
    """
    Load schedule for all groups to work offline.
    """

    con = sqlite3.connect(cache_file)
    cur = con.cursor()

    for i, group in enumerate(iter_groups()):
        print(f'Processing group {group["name"]}')

        timestamp = int(time.time())
        schedule = get_group_schedule(group['id'], date_start, date_end)

        # Prepare data for inserting into cache
        values = []
        for day in schedule:
            values.append((
                group['id'],
                day['date'],
                json.dumps(day['lessons'], ensure_ascii=False),
                timestamp,
            ))

        # Insert data into cache
        cur.executemany('INSERT OR REPLACE INTO group_schedule VALUES (?, ?, ?, ?)', values)

        # Flush data to cache file
        if i % DB_FLUSH_INTERVAL == 0:
            print(f'Flushing data to cache file... #{i // DB_FLUSH_INTERVAL + 1}')
            con.commit()

    con.commit()
    con.close()
    print('Done!')


def iter_groups() -> Generator[Dict, None, None]:
    """
    Iterate over all groups in university.
    """

    for structure in get_structures():
        for faculty in get_faculties(structure['id']):
            for course in get_courses(faculty['id']):
                for group in get_groups(faculty['id'], course['course']):
                    yield group


def get_structures() -> List[Dict]:
    """
    Get structures list from university api.
    """
    return _make_api_request('/list/structures')


def get_faculties(structure_id: int) -> List[Dict]:
    """
    Get faculties list from university api.
    """
    return _make_api_request('/list/faculties', method='POST', json_={'structureId': structure_id})


def get_courses(faculty_id: int) -> List[Dict]:
    """
    Get courses list from university api.
    """
    return _make_api_request('/list/courses', method='POST', json_={'facultyId': faculty_id})


def get_groups(faculty_id: int, course: int) -> List[Dict]:
    """
    Get groups list from university api.
    """
    return _make_api_request('/list/groups', method='POST', json_={'facultyId': faculty_id, 'course': course})


def get_group_schedule(group_id: int, date_start: str, date_end: str) -> List[Dict]:
    """
    Get schedule for group from university api.
    """
    res = _make_api_request('/time-table/group', method='POST', json_={
        'groupId': group_id,
        'dateStart': date_start,
        'dateEnd': date_end,
        })
    
    _fill_empty_dates(res, date.fromisoformat(date_start), date.fromisoformat(date_end))
    return res


def _make_api_request(path: str, method: str = 'GET', json_: Optional[Dict] = None) -> Dict:
    """
    Make request to university api.
    """

    http = urllib3.PoolManager()
    url = f'{API_URL}{path}'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Language': 'uk'
    }

    if method == 'GET':
        response = http.request(method, url, headers=headers)
    elif method == 'POST':
        response = http.request(method, url, body=json.dumps(json_), headers=headers)
    else:
        raise Exception(f'Unknown method: {method}')

    if response.status != 200:
        raise Exception(f'Got {response.status} status code from api: {response.data.decode()}')

    return json.loads(response.data.decode())


def _fill_empty_dates(schedule: list[dict], from_date: date, to_date: date) -> list[dict]:
    """Fill empty dates in schedule

    For example, we have schedule for 2023-08-21 and 2023-08-23.
    If there is no lessons for 2023-08-22, API will return schedule only for 2023-08-21 and 2023-08-23.
    This function will fill empty dates with empty lessons list.
    """

    i = 0
    expected_date = from_date
    while expected_date <= to_date:
        if i < len(schedule):
            date_ = date.fromisoformat(schedule[i]['date'])

            if date_ < expected_date:
                # This shouldn't really happen, but there have been a few cases where
                # for some reason api returned schedule for days we didn't even request.
                i += 1
                continue

        if i >= len(schedule) or date_ > expected_date:
            schedule.insert(i, {
                'date': expected_date.isoformat(),
                'lessons': []
            })

        i += 1
        expected_date = expected_date + timedelta(days=1)

    return schedule


if __name__ == '__main__':
    # Parse cli arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--file', type=str, help='Path to api cache file (api.sqlite)')
    parser.add_argument('--from', type=str, dest='from_', help='Start date for schedule', required=True)
    parser.add_argument('--to', type=str, help='End date for schedule', required=True)
    args = parser.parse_args()

    if args.file is None:
        # Search for api cache file
        paths = ('./', './cache/')
        fname = 'api.sqlite'

        for cache_file in paths:
            if os.path.exists(os.path.join(cache_file, fname)):
                args.file = os.path.join(cache_file, fname)
                break
        else:
            print('Could not find api cache file. Please specify it using --file argument.')
            exit(1)

    main(args.file, args.from_, args.to)
