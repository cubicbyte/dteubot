from dataclasses import dataclass

@dataclass
class CallSchedule:
    timeStart:  str
    timeEnd:    str
    number:     int
    length:     int

@dataclass
class Chair:
    id:         int
    shortName:  str
    fullName:   str

@dataclass
class Classroom:
    id:         int
    name:       str
    countPlace: int
    type:       int

@dataclass
class Course:
    course: int

@dataclass
class Faculty:
    id:         int
    shortName:  str
    fullName:   str

@dataclass
class Group:
    id:             int
    name:           str
    course:         int
    priority:       int
    educationForm:  int

@dataclass
class Person:
    id:         int
    firstName:  str
    secondName: str
    lastName:   str

@dataclass
class Rd:
    html: str

@dataclass
class Structure:
    id:         int
    shortName:  str
    fullName:   str

@dataclass
class Student:
    id: int
    firstName:  str
    secondName: str
    lastName:   str

@dataclass
class TeacherByName:
    chairName:  str
    id:         int
    firstName:  str
    secondName: str
    lastName:   str

@dataclass
class TimeTablePeriod:
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
    type:                   int
    typeStr:                str # For some reason this field is missing in the documentation
    dateUpdated:            str
    nonstandartTime:        bool
    groups:                 str
    extraText:              bool

@dataclass
class TimeTableLesson:
    number:         int
    periods:        list[TimeTablePeriod]

@dataclass
class TimeTableDate:
    date:       str
    lessons:    list[TimeTableLesson]

@dataclass
class TeacherIdentifier:
    id:     int
    hash:   str

@dataclass
class StudentIdentifier:
    id:     int
    hash:   str

@dataclass
class UniversalLesson:
    r1:                     int
    date:                   str
    number:                 int
    rz14:                   int
    rz15:                   int
    r5:                     int
    ucx5:                   int
    disciplineId:           int
    educationDisciplineId:  int
    disciplineFullName:     str
    disciplineShortName:    str
    classroom:              str
    timeStart:              str
    timeEnd:                str
    type:                   int
    dateUpdated:            str
    nonstandardTime:        bool
    groups:                 list[int]
    extraText:              bool
    teachers:               list[TeacherIdentifier]
    otherStudents:          list[StudentIdentifier]

@dataclass
class Version:
    name: str
    code: str
