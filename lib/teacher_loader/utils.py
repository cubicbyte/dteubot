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


def convert_latin_to_cyrillic(string: str) -> str:
    """Replace latin characters from cyrillic string with cyrillic characters (a, o, i, e, ...)"""
    letters = (
        'eiopaxc',  # latin
        'еіорахс',  # cyrillic
        # 'eiopaxcETIOPAHKXCBM',  # latin
        # 'еіорахсЕТІОРАНКХСВМ',  # cyrillic
    )

    for latin, cyrillic in zip(*letters):
        string = string.replace(latin, cyrillic)

    return string
