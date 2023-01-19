import sqlite3
from datetime import date

class CacheReader:
    def __init__(self, file: str) -> None:
        self.__connection = sqlite3.connect(file)

    def __example(self):
        con = self.__connection
        cur = con.cursor()
        cur.execute('SELECT * FROM Schedule LIMIT 1')
        res = cur.fetchone()
        print(res)

    def get_schedule(self, groupId: int, date: str | date) -> list[dict] | None:
        pass

    def get_structures(self) -> list[dict] | None:
        pass

    def get_faculties(self, structureId: int) -> list[dict] | None:
        pass

    def get_courses(self, facultyId: int) -> list[dict] | None:
        pass

    def get_groups(self, facultyId: int, course: int) -> list[dict] | None:
        pass
