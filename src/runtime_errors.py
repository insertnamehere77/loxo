from typing import Any
from lox_token import TokenType, Token

# Normally I would put these in interpreter.py but the resolver and environment classes can also raise these
class LoxRuntimeError(Exception):
    message: str
    line: int

    def __init__(self, message: str, token: Token) -> None:
        self.message = message
        self.line = token.line

    def __str__(self) -> str:
        return f"Line {self.line}: {self.message}"


class InvalidOperatorError(LoxRuntimeError):
    operator: TokenType
    values: tuple[Any]

    def __init__(self, operator: Token, *values: Any) -> None:
        super().__init__(
            f'Cannot apply operator {operator.token_type.value} to value(s) {",".join(str(values))}',
            operator,
        )
        self.operator = operator.token_type
        self.values = values
