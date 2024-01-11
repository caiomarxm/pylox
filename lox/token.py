from .token_type import TokenType

class Token: 
    def __init__(self, type:TokenType, lexeme:str, literal, line:int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"Type: {self.type}, lexeme: {self.lexeme}, literal: {self.literal}"
