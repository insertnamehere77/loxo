from lox_token import Token, TokenType
from result import Result
from typing import Any


class BaseScannerError(Exception):
    line: int

    def __init__(self, line: int) -> None:
        super().__init__()
        self.line = line


class UnterminatedStringError(BaseScannerError):
    message: str

    def __init__(self, line: int) -> None:
        super().__init__(line)
        self.message = 'Unterminated string, expected closing " on line {}'.format(line)

    def __repr__(self) -> str:
        return "UnterminatedStringError: {}".format(self.message)


class UnexpectedCharError(BaseScannerError):
    message: str
    char: str

    def __init__(self, line: int, char: str) -> None:
        super().__init__(line)
        self.char = char
        self.message = "Unexepected character {} at line {}".format(char, line)

    def __repr__(self) -> str:
        return "UnexpectedCharError: {}".format(self.message)


class Scanner:
    source_code: str
    curr_index: int
    line_num: int
    tokens: list[Token]
    errors: list[Exception]

    def __init__(self, source: str) -> None:
        self.source_code = source
        self.line_num = 1
        self.curr_index = 0
        self.tokens = []
        self.errors = []

    def _is_at_end(self) -> bool:
        return len(self.source_code) <= self.curr_index

    def _advance(self) -> str:
        char = self.source_code[self.curr_index]

        self.curr_index += 1
        if char == "\n":
            self.line_num += 1

        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False

        char = self.source_code[self.curr_index]
        if char != expected:
            return False

        self.curr_index += 1
        return True

    def _add_token(self, type: TokenType, val: Any = None):
        self.tokens.append(Token(type, val))

    def _add_error(self, err: BaseScannerError):
        self.errors.append(err)

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source_code[self.curr_index]

    def _peek_next(self) -> str:
        if len(self.source_code) <= (self.curr_index + 1):
            return "\0"
        return self.source_code[self.curr_index + 1]

    def _handle_string(self):
        lex_start = self.curr_index
        while (self._peek() != '"') and (not self._is_at_end()):
            self._advance()

        if self._is_at_end():
            self._add_error(UnterminatedStringError(self.line_num))
            return

        self._advance()

        val = self.source_code[lex_start : self.curr_index - 1]
        self._add_token(TokenType.STRING, val)

    def _handle_number(self):
        lex_start = self.curr_index - 1
        while self._peek().isdigit():
            self._advance()

        if (self._peek() == ".") and (self._peek_next().isdigit()):
            self._advance()

            while self._peek().isdigit():
                self._advance()

        val_str = self.source_code[lex_start : self.curr_index]
        self._add_token(TokenType.NUMBER, float(val_str))

    def _handle_identifier_or_keyword(self):
        lex_start = self.curr_index - 1
        while (self._peek().isalnum()) or (self._peek() == "_"):
            self._advance()

        name = self.source_code[lex_start : self.curr_index]
        self._add_token(
            TokenType(name)
            if TokenType.is_keyword_token(name)
            else TokenType.IDENTIFIER,
            name,
        )

    def scan_tokens(self) -> Result:
        while not self._is_at_end():
            char = self._advance()

            if char.isspace():
                pass

            elif TokenType.is_one_char_token(char):
                type = TokenType(char)
                self._add_token(type)

            elif TokenType.is_token_combinable_with_equal(char):
                type = TokenType((char + "=") if self._match("=") else char)
                self._add_token(type)

            elif char == "/":
                if self._match("/"):
                    while (self._peek() != "\n") and (not self._is_at_end()):
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)

            elif char == '"':
                self._handle_string()

            else:
                if char.isdigit():
                    self._handle_number()
                elif char.isalpha():
                    self._handle_identifier_or_keyword()
                else:
                    self._add_error(UnexpectedCharError(self.line_num, char))

        if len(self.errors) > 0:
            return Result.Fail(self.errors)

        return Result.Ok(self.tokens)
