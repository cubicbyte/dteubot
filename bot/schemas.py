
class Language(dict):
    """
    A wrapper around a language dictionary.
    If a key is not present in the dictionary, it returns the key itself.
    """

    def __init__(
            self,
            lang: Optional[dict[str, str]],
            code: Optional[str]
    ):
        """
        :param lang: Language dictionary
        :param code: Language code
        """

        super().__init__(lang or {})

        self.lang_code: str | None = code
        "Language code"

    def __str__(self) -> str | None:
        return self.lang_code

    def __missing__(self, __key: str) -> str:
        return __key

    def get(self, __key: str) -> str:
        return self[__key]
