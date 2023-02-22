from functools import lru_cache
from ..settings import langs

@lru_cache
def create_message(lang_code: str) -> dict:
    message_text = langs[lang_code]['page.greeting']

    msg = {
        'text': message_text,
        'parse_mode': 'MarkdownV2'
    }

    return msg
