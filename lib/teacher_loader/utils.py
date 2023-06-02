import re


def format_string(s: str) -> str:
    """Remove unnecessary characters from string"""
    s = re.sub(r'[^\S ]', ' ', s)   # remove all whitespace characters except space
    s = re.sub(' +', ' ', s)        # remove extra spaces
    return s.strip()
