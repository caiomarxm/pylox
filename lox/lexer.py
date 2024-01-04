from .token import Token
from .token_type import TokenType as tt


class Lexer:
    source:str
    tokens:list[Token]
    start = 0
    current = 0
    line = 1


    def __init__(self, source:str) -> None:
        self.source:str = source


    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(tt.EOF, "", None, self.line))
        
        return []


    def scan_token(self):
        c = self.advance()

        match c:
            case '(': self.add_token(tt.LEFT_PAREN)
            case ')': self.add_token(tt.RIGHT_PAREN)
            case '{': self.add_token(tt.LEFT_BRACE)
            case '}': self.add_token(tt.RIGHT_BRACE)
            case ',': self.add_token(tt.COMMA)
            case '.': self.add_token(tt.DOT)
            case '-': self.add_token(tt.MINUS)
            case '+': self.add_token(tt.PLUS)
            case ';': self.add_token(tt.SEMICOLON)
            case '*': self.add_token(tt.STAR)


    def is_at_end(self):
        return self.current >= len(self.source)


    def advance(self) -> str:
        return self.source[self.current+1]


    def add_token(self, type:tt, literal=None) -> None:
        text = self.source[self.start, self.current]
        self.tokens.append(Token(type, text, literal, self.line))
