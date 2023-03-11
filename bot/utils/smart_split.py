from typing import List

MAX_MESSAGE_LENGTH = 4096

# Copied from the pyTelegramBotApi library
# Link: https://github.com/eternnoir/pyTelegramBotAPI/blob/5d9a76b0dd0d3ee88c5c9d1329c06b24fdc4457b/telebot/util.py#L327
def smart_split(text: str, chars_per_string: int = MAX_MESSAGE_LENGTH) -> List[str]:
    r"""
    Splits one string into multiple strings, with a maximum amount of `chars_per_string` characters per string.
    This is very useful for splitting one giant message into multiples.
    If `chars_per_string` > 4096: `chars_per_string` = 4096.
    Splits by '\n', '. ' or ' ' in exactly this priority.
    :param text: The text to split
    :type text: :obj:`str`
    :param chars_per_string: The number of maximum characters per part the text is split to.
    :type chars_per_string: :obj:`int`
    :return: The splitted text as a list of strings.
    :rtype: :obj:`list` of :obj:`str`
    """

    def _text_before_last(substr: str) -> str:
        return substr.join(part.split(substr)[:-1]) + substr

    if chars_per_string > MAX_MESSAGE_LENGTH: chars_per_string = MAX_MESSAGE_LENGTH

    parts = []
    while True:
        if len(text) < chars_per_string:
            parts.append(text)
            return parts

        part = text[:chars_per_string]

        if "\n" in part:
            part = _text_before_last("\n")
        elif ". " in part:
            part = _text_before_last(". ")
        elif " " in part:
            part = _text_before_last(" ")

        parts.append(part)
        text = text[len(part):]
