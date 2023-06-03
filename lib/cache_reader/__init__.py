import sqlite3
from datetime import date as _date


class CacheReader:
    def __init__(self, file: str) -> None:
        self.__connection = sqlite3.connect(file, check_same_thread=False)

    def get_schedule(self, groupId: int, dateStart: _date | str,
                     dateEnd: _date | str = None) -> list[list] | None:

        if type(dateStart) == _date:
            dateStart = dateStart.isoformat()
        if dateEnd is None:
            dateEnd = dateStart
        elif type(dateEnd) == _date:
            dateEnd = dateEnd.isoformat()

        cur = self.__connection.cursor()
        cur.execute('SELECT * FROM Schedule WHERE groupId = ? AND date BETWEEN ? AND ?;',
                    (groupId, dateStart, dateEnd))
        res = cur.fetchall()
        cur.close()
        return res

    def get_structures(self) -> list[list]:
        cur = self.__connection.cursor()
        cur.execute('SELECT * FROM Structures;')
        res = cur.fetchall()
        cur.close()
        return res

    def get_faculties(self, structureId: int) -> list[list]:
        cur = self.__connection.cursor()
        cur.execute('SELECT * FROM Faculties WHERE structureId = ?;', (structureId,))
        res = cur.fetchall()
        cur.close()
        return res

    def get_courses(self, facultyId: int) -> list[list]:
        cur = self.__connection.cursor()
        cur.execute('SELECT * FROM Courses WHERE facultyId = ?;', (facultyId,))
        res = cur.fetchall()
        cur.close()
        return res

    def get_groups(self, facultyId: int, course: int) -> list[list]:
        cur = self.__connection.cursor()
        cur.execute('SELECT * FROM Groups WHERE facultyId = ? AND course = ?;', (facultyId, course))
        res = cur.fetchall()
        cur.close()
        return res

    def get_group(self, groupId: int) -> list | None:
        cur = self.__connection.cursor()
        cur.execute('SELECT * FROM Groups WHERE id = ?;', (groupId,))
        res = cur.fetchone()
        cur.close()
        return res
