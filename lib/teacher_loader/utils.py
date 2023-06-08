"""
Utility functions
"""

import regex


def format_string(string: str) -> str:
    """Remove unnecessary characters from string"""
    string = regex.sub(r'[^\S ]', ' ', string)  # remove all whitespace characters except space
    string = regex.sub(' +', ' ', string)       # remove extra spaces
    string = regex.sub(r'\p{C}', '', string)    # remove even more garbage characters, like zero-width space
    return string.strip()
