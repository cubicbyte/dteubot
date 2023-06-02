from datetime import datetime, timedelta
from dataclasses import dataclass, field as _field


class Language(dict):
    """
    A wrapper around a language dictionary.
    If a key is not present in the dictionary, it returns the key itself.
    """

    def __init__(
            self,
            lang: dict[str, str] | None = None,
            name: str | None = None
    ):
        """
        :param lang: Language dictionary
        :param name: Language name
        """

        super().__init__(lang or {})

        self.name: str | None = name
        "Language name"

    def __str__(self) -> str | None:
        return self.name

    def __missing__(self, __key: str) -> str:
        return __key

    def get(self, __key: str) -> str:
        return self[__key]


@dataclass(frozen=True)
class StoredMessage:
    """A message stored in the bot database"""

    id: int
    timestamp: datetime
    page_name: str
    lang_code: str
    data: dict[str, any] = _field(default_factory=dict)
