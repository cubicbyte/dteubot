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
