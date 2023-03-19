from typing import List
from dataclasses import dataclass

class JSONDeserializable:
    @classmethod
    def from_json(cls, raw: dict | List[dict]) -> 'JSONDeserializable':
        if isinstance(raw, list):
            return [cls(**r) for r in raw]
        return cls(**raw)


@dataclass
class CallSchedule(JSONDeserializable):
    "Моделька для пар"
    timeStart: str
    "Время начала"
    timeEnd: str
    "Время конца"
    number: int
    "Номер"
    length: int
    "Длительность"

@dataclass
class Chair(JSONDeserializable):
    "Моделька для кафедр"
    id: int
    "id кафедры"
    shortName: str
    "Аббревиатура кафедры"
    fullName: str
    "Название кафедры"

@dataclass
class Classroom(JSONDeserializable):
    "Моделька для учебных аудиторий"
    id: int
    "id аудитории"
    name: str
    "Название аудитории"
    countPlace: int
    "Количество мест"
    type: int
    "Тип 0-учебная 1-лаборатория"

@dataclass
class Course(JSONDeserializable):
    "Моделька для курсов"
    course: int
    "Курс"

@dataclass
class Faculty(JSONDeserializable):
    "Моделька для факультетов"
    id: int
    "id факультета"
    shortName: str
    "Аббревиатура факультета(Зависит от языка приложения)"
    fullName: str
    "Название факультета(Зависит от языка приложения)"

@dataclass
class Group(JSONDeserializable):
    "Моделька для групп"
    id: int
    "id группы"
    name: str
    "Название группы"
    course: int
    "Курс группы"
    priority: int
    "Приоритет вывода"
    educationForm: int
    "Форма обучения"

@dataclass
class Person(JSONDeserializable):
    "Моделька для персон"
    id: int
    "id преподавателя"
    firstName: str
    "Имя преподавателя"
    secondName: str
    "Отчество преподавателя"
    lastName: str
    "Фамилия преподавателя"

@dataclass
class Rd(JSONDeserializable):
    "Моделька для объявлений в расписании"
    html: str
    "Объявление"

@dataclass
class Structure(JSONDeserializable):
    "Моделька для структур"
    id: int
    "id структуры"
    shortName: str
    "Аббревиатура структуры(Зависит от языка приложения)"
    fullName: str
    "Название структуры(Зависит от языка приложения)"

@dataclass
class Student(JSONDeserializable):
    "Моделька для Студентов"
    id: int
    "id студента"
    firstName: str
    "Имя студента"
    secondName: str
    "Отчество студента"
    lastName: str
    "Фамилия студента"

@dataclass
class TeacherByName(JSONDeserializable):
    "Моделька для поиска преподавателя"
    chairName: str
    "Название кафедры"
    id: int
    "id преподавателя"
    firstName: str
    "Имя преподавателя"
    secondName: str
    "Отчество преподавателя"
    lastName: str
    "Фамилия преподавателя"

@dataclass
class TimeTablePeriod(JSONDeserializable):
    "Моделька для занятия в расписании"
    r1: int
    "Код занятия"
    rz14: int # По шапке бы надавал за такие названия
    rz15: int
    r5: int
    disciplineId: int
    "Идентификатор глобальной дисциплины"
    educationDisciplineId: int
    "Идентификатор дисциплины учебного плана"
    disciplineFullName: str
    "Полное название дисциплины"
    disciplineShortName: str
    "Сокращенное название дисциплины"
    classroom: str
    "Название аудитории"
    timeStart: str
    "Время начала"
    timeEnd: str
    "Время конца"
    teachersName: str
    "Сокращенные имена преподавателей"
    teachersNameFull: str
    "ФИО преподавателей"
    chairName: str # Missing in the docs
    "Название кафедры"
    type: int
    "Тип занятия"
    typeStr: str # Missing in the docs
    "Тип занятия (строковый формат)"
    dateUpdated: str
    "Дата последнего обновления"
    nonstandardTime: bool
    "Нестандартное время занятия"
    groups: str
    "Названия групп"
    extraText: bool
    "Есть ли объявление"

@dataclass
class TimeTableLesson(JSONDeserializable):
    "Моделька для пары в расписании"
    number: int
    "Номер занятия"
    periods: list[TimeTablePeriod]
    "Список занятий"

    @staticmethod
    def from_json(raw: dict | List[dict]) -> 'TimeTableLesson' | List['TimeTableLesson']:
        if isinstance(raw, list):
            res = []
            for r in raw:
                periods = TimeTablePeriod.from_json(r['periods'])
                del r['periods']
                res.append(TimeTableLesson(**r, periods=periods))
            return res
        periods = TimeTablePeriod.from_json(raw['periods'])
        del raw['periods']
        return TimeTableLesson(**raw, periods=periods)

@dataclass
class TimeTableDate(JSONDeserializable):
    "Моделька для дня в расписании"
    date: str
    "Дата"
    lessons: list[TimeTableLesson]
    "Список пар"

    @staticmethod
    def from_json(raw: dict | List[dict]) -> 'TimeTableDate' | List['TimeTableDate']:
        if isinstance(raw, list):
            res = []
            for r in raw:
                lessons = TimeTableLesson.from_json(r['lessons'])
                del r['lessons']
                res.append(TimeTableDate(**r, lessons=lessons))
            return res
        lessons = TimeTableLesson.from_json(raw['lessons'])
        del raw['lessons']
        return TimeTableDate(**raw, lessons=lessons)

@dataclass
class TeacherIdentifier(JSONDeserializable):
    "Моделька для преподавателей (связь с другими системами)"
    id: int
    "id преподавателя"
    hash: str
    "Hash"

@dataclass
class StudentIdentifier(JSONDeserializable):
    "Моделька для студента (связь с другими системами)"
    id: int
    "id обучения студента"
    hash: str
    "Hash"

@dataclass
class Version(JSONDeserializable):
    "Моделька для версии"
    name: str
    "Версия"
    code: str
    "Код версии"
