from .token import Token
from .token_type import TokenType as tt


class Lexer:
    source:str
    tokens:list[Token]
    start = -1
    current = -1
    line = 1


    def __init__(self, source:str, error_function:callable) -> None:
        self.source:str = source
        self.error = error_function
        self.tokens = []


    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(tt.EOF, "", None, self.line))
        
        return self.tokens


    def scan_token(self):
        c = self.advance()

        match c:
            # Single-character tokens
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
            # Slash must handle comments
            case '/':
                if self.match_next('/'):
                    while self.source[self.current] != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(tt.SLASH)

            # One or two character tokens
            case '!':
                self.add_token(
                    tt.BANG_EQUAL if self.match_next('=') else tt.BANG,
                )
            case '=':
                self.add_token(
                    tt.EQUAL_EQUAL if self.match_next('=') else tt.EQUAL,
                )
            case '<':
                self.add_token(
                    tt.LESS_EQUAL if self.match_next('=') else tt.LESS,
                )
            case '>':
                self.add_token(
                    tt.GREATER_EQUAL if self.match_next('=') else tt.GREATER,
                )
            
            # Reading string literals
            case '"':
                self.read_string()

            case _:
                # Reading numbers
                if self.is_digit(c):
                    self.read_number()

                # Identifiers
                elif self.is_alpha(c):
                    self.read_identifier()

                else:
                    self.error(self.line, f"Unexpected character ' {c} '.")


    def read_identifier(self):
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        
        self.add_token(tt.IDENTIFIER)

    
    def read_number(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        # Looking for fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(
            tt.NUMBER,
            float(self.source[self.start+1 : self.current+1])
            )


    def read_string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        
        if self.is_at_end():
            self.error(self.line, f"Unterminated string.")
            return
        
        self.advance()

        value = self.source[self.start+2 : self.current]
        self.add_token(tt.STRING, value)
        
    
    def match_next(self, expected:str) -> bool:
        if self.is_at_end():
            return False
        
        if self.source[self.current+1] != expected:
            return False
        
        self.current += 1

        return True


    def peek(self) -> str:
        """Look ahead without consuming characters
        """
        if self.is_at_end():
            return '\0'
        return self.source[self.current+1]
    

    def peek_next(self) -> str:
        if self.current+2 >= len(self.source):
            return '\0'
        return self.source[self.current+2]

    
    def is_alpha(self, char:str) -> bool:
        return (
            char >= 'a' and char <= 'z' or
            char >= 'A' and char <= 'Z' or
            char == '_'
        )
    

    def is_alpha_numeric(self, char:str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)


    def is_digit(self, char:str) -> bool:
        return char >= '0' and char <= '9'


    def is_at_end(self) -> bool:
        return self.current >= len(self.source)-1 # -1 corrects index problems


    def advance(self) -> str:
        self.current += 1
        return self.source[self.current]


    def add_token(self, type:tt, literal=None) -> None:
        text = self.source[self.start+1 : self.current+1]
        self.tokens.append(Token(type, text, literal, self.line))
