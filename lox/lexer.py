from .token import Token


class Lexer:
    def __init__(self, source:str) -> None:
        self._source = source
        pass

    def scan_tokens(self) -> list[Token]:
        return []
