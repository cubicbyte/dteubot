def check_int(s: str) -> bool:
    'Check if a string is an integer'
    if s[0] == '-' or s[0] == '+':
        return s[1:].isdigit()
    return s.isdigit()
