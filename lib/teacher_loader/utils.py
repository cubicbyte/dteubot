"""
Utility functions
"""

import re


def format_string(string: str) -> str:
    """Remove unnecessary characters from string"""
    string = re.sub(r'[^\S ]', ' ', string)   # remove all whitespace characters except space
    string = re.sub(' +', ' ', string)        # remove extra spaces
    return string.strip()
