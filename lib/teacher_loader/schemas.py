"""
Schemas module
"""

from dataclasses import dataclass


@dataclass
class Chair:
    """Chair info"""

    name: str
    page_link: str


@dataclass
class Faculty:
    """Faculty info"""

    name: str
    chairs: list[Chair]


@dataclass
class Teacher:
    """Short teacher info"""

    name: str
    description: str
    photo_link: str
    page_link: str


@dataclass
class FullTeacher:
    """Full teacher info"""

    name: setattr
    label: str
    description: str
    photo_link: str
    email: str
    social_links: list[str]
    research_interests: list[str]
    disciplines: list[str]
    academic_qualifications: list[str]
    work_experience: list[str]
    awards_and_honors: list[str]
    advanced_training: list[str]
    additional_activities: list[str]
    hobbies: list[str]
