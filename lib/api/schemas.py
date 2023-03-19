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
    timeStart:  str
    timeEnd:    str
    number:     int
    length:     int

@dataclass
class Chair(JSONDeserializable):
    id:         int
    shortName:  str
    fullName:   str

@dataclass
class Classroom(JSONDeserializable):
    id:         int
    name:       str
    countPlace: int
    type:       int

@dataclass
class Course(JSONDeserializable):
    course: int

@dataclass
class Faculty(JSONDeserializable):
    id:         int
    shortName:  str
    fullName:   str

@dataclass
class Group(JSONDeserializable):
    id:             int
    name:           str
    course:         int
    priority:       int
    educationForm:  int

@dataclass
class Person(JSONDeserializable):
    id:         int
    firstName:  str
    secondName: str
    lastName:   str

@dataclass
class Rd(JSONDeserializable):
    html: str

@dataclass
class Structure(JSONDeserializable):
    id:         int
    shortName:  str
    fullName:   str

@dataclass
class Student(JSONDeserializable):
    id: int
    firstName:  str
    secondName: str
    lastName:   str

@dataclass
class TeacherByName(JSONDeserializable):
    chairName:  str
    id:         int
    firstName:  str
    secondName: str
    lastName:   str

@dataclass
class TimeTablePeriod(JSONDeserializable):
    r1:                     int
    rz14:                   int
    rz15:                   int
    r5:                     int
    disciplineId:           int
    educationDisciplineId:  int
    disciplineFullName:     str
    disciplineShortName:    str
    classroom:              str
    timeStart:              str
    timeEnd:                str
    teachersName:           str
    teachersNameFull:       str
    chairName:              str
    type:                   int
    typeStr:                str # For some reason this field is missing in the documentation
    dateUpdated:            str
    nonstandardTime:        bool
    groups:                 str
    extraText:              bool

@dataclass
class TimeTableLesson(JSONDeserializable):
    number:         int
    periods:        list[TimeTablePeriod]

    @staticmethod
    def from_json(raw: dict | List[dict]):
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
    date:       str
    lessons:    list[TimeTableLesson]

    @staticmethod
    def from_json(raw: dict | List[dict]):
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
    id:     int
    hash:   str

@dataclass
class StudentIdentifier(JSONDeserializable):
    id:     int
    hash:   str

@dataclass
class Version(JSONDeserializable):
    name: str
    code: str
