from stmt import Print, Stmt, Expression, Var, Block
from types import FunctionType
from lox_token import Token, TokenType
from expr import Binary, Expr, Grouping, Unary, Literal, Variable, Assign
from result import Result


class ParseError(Exception):
    token: Token
    message: str

    def __init__(self, token: Token, err_msg: str) -> None:
        super().__init__()
        self.token = token
        self.message = err_msg


class Parser:
    tokens: list[Token]
    curr_index: int
    errors: list[ParseError]

    def __init__(self, tokens: list[Token]) -> None:
        self.curr_index = 0
        self.tokens = tokens
        self.errors = []

    def parse(self) -> Result[list[Stmt], list[ParseError]]:

        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())

        if len(self.errors) > 0:
            return Result.Fail(self.errors)

        return Result.Ok(statements)

    def _declaration(self) -> Stmt:
        try:
            if self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except ParseError:
            self._synchronize()

    def _var_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, "Expected variabled name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return Var(name, initializer)

    def _statement(self) -> Stmt:
        if self._match(TokenType.PRINT):
            return self._print_statement()

        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())

        return self._expression_statement()

    def _block(self) -> list[Stmt]:
        statements = []
        while (not self._check(TokenType.RIGHT_BRACE)) and (not self._is_at_end()):
            statements.append(self._declaration())

        self._consume(TokenType.RIGHT_BRACE, "Expected '}' after block")
        return statements

    def _print_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return Print(value)

    def _expression_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return Expression(value)

    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._equality()
        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()

            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)

            raise self._error(equals, "Invalid assignment")
        return expr

    def _equality(self) -> Expr:
        return self._match_left_associate(
            self._comparison, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL
        )

    def _match_left_associate(self, operand_method: FunctionType, *types: TokenType):
        expr = operand_method()

        while self._match(*types):
            operator = self._previous()
            right = operand_method()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        return self._match_left_associate(
            self._term,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        )

    def _term(self) -> Expr:
        return self._match_left_associate(self._factor, TokenType.MINUS, TokenType.PLUS)

    def _factor(self) -> Expr:
        return self._match_left_associate(self._unary, TokenType.SLASH, TokenType.STAR)

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)

        return self._primary()

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().value)

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, type: TokenType, err_msg: str) -> Expr:
        if self._check(type):
            return self._advance()

        raise self._error(self._peek(), err_msg)

    def _error(self, token: Token, err_msg: str) -> Exception:
        err = ParseError(token, err_msg)
        self.errors.append(err)
        return err

    def _synchronize(self):
        self._advance()

        while not self._is_at_end():
            if self._previous().token_type == TokenType.SEMICOLON:
                return

            if self._peek().token_type in [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN,
            ]:
                return

            self._advance()

    def _match(self, *types: TokenType) -> bool:
        for type in types:
            if self._check(type):
                self._advance()
                return True

        return False

    def _check(self, type: TokenType) -> bool:
        if self._is_at_end():
            return False

        return self._peek().token_type == type

    def _is_at_end(self) -> bool:
        return self._peek().token_type == TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.curr_index]

    def _previous(self) -> Token:
        return self.tokens[self.curr_index - 1]

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.curr_index += 1
        return self._previous()
