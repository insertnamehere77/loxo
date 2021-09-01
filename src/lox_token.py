from enum import Enum, auto
from typing import Any

# Had to name this lox_token so python doesn't get confused with it's own token module


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"

    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    STAR = "*"

    # Could also be start of a comment
    SLASH = "/"

    # One or two character tokens
    BANG = "!"
    BANG_EQUAL = "!="

    EQUAL = "="
    EQUAL_EQUAL = "=="

    GREATER = ">"
    GREATER_EQUAL = ">="

    LESS = "<"
    LESS_EQUAL = "<="

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"

    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = auto()

    def is_one_char_token(char: str) -> bool:
        single_char_tokens = {
            TokenType.LEFT_PAREN.value,
            TokenType.RIGHT_PAREN.value,
            TokenType.LEFT_BRACE.value,
            TokenType.RIGHT_BRACE.value,
            TokenType.COMMA.value,
            TokenType.DOT.value,
            TokenType.MINUS.value,
            TokenType.PLUS.value,
            TokenType.SEMICOLON.value,
            TokenType.STAR.value,
        }
        return char in single_char_tokens

    def is_token_combinable_with_equal(char: str) -> bool:
        tokens_combinable_with_equal = {
            TokenType.BANG.value,
            TokenType.EQUAL.value,
            TokenType.GREATER.value,
            TokenType.LESS.value,
        }
        return char in tokens_combinable_with_equal

    def is_keyword_token(char: str) -> bool:
        keyword_tokens = {
            TokenType.AND.value,
            TokenType.CLASS.value,
            TokenType.ELSE.value,
            TokenType.FALSE.value,
            TokenType.FUN.value,
            TokenType.FOR.value,
            TokenType.IF.value,
            TokenType.NIL.value,
            TokenType.OR.value,
            TokenType.PRINT.value,
            TokenType.RETURN.value,
            TokenType.SUPER.value,
            TokenType.THIS.value,
            TokenType.TRUE.value,
            TokenType.VAR.value,
            TokenType.WHILE.value,
        }
        return char in keyword_tokens


class Token:
    token_type: TokenType
    value: Any

    def __init__(self, type: TokenType, val: Any) -> None:
        self.token_type = type
        self.value = val

    def __repr__(self) -> str:
        return "{}, val: {}".format(self.token_type, self.value)
