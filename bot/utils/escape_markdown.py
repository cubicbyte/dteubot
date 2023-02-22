def _escape_str(text: str, escape_chars: str, prefix = '\\') -> str:
    for char in escape_chars:
        text = text.replace(char, prefix + char)

    return text

def escape_markdown(text: str) -> str:
    """
    Function for escaping telegram markdown V2 text

    Markdown style: https://core.telegram.org/bots/api#markdown-style
    """
    escape_chars = "_*`["
    return _escape_str(text, escape_chars)

def escape_markdownv2(text: str) -> str:
    """
    Function for escaping telegram markdown V2 text

    MarkdownV2 style: https://core.telegram.org/bots/api#markdownv2-style
    """
    escape_chars = "_*[]()~`>#+-=|{}.!"
    return _escape_str(text, escape_chars)
