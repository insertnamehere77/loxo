from stmt import Print, Stmt, Expression, Var, Block, If, While, Fun, Return, LoxClass
from types import FunctionType
from lox_token import Token, TokenType
from expr import (
    Binary,
    Expr,
    Grouping,
    Unary,
    Literal,
    Variable,
    Assign,
    Logical,
    Call,
    Get,
    Set,
    This,
    Super,
)
from result import Result


class ParseError(Exception):
    token: Token
    message: str

    def __init__(self, token: Token, err_msg: str) -> None:
        super().__init__()
        self.token = token
        self.message = f"Line {token.line}: {err_msg}"


_MAX_NUM_ARGS = 255


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
            if self._match(TokenType.CLASS):
                return self._class_declaration()
            if self._match(TokenType.FUN):
                return self._function("function")
            if self._match(TokenType.VAR):
                return self._var_declaration()
            return self._statement()
        except ParseError:
            self._synchronize()

    def _class_declaration(self):
        name = self._consume(TokenType.IDENTIFIER, "Expected class name")

        superclass = None
        if self._match(TokenType.LESS):
            self._consume(TokenType.IDENTIFIER, "Expected superclass name")
            superclass = Variable(self._previous())

        self._consume(TokenType.LEFT_BRACE, "Expected opening { before class body")

        methods = []
        while (not self._check(TokenType.RIGHT_BRACE)) and (not self._is_at_end()):
            methods.append(self._function("method"))

        self._consume(TokenType.RIGHT_BRACE, "Expected closing } after class body")
        return LoxClass(name, superclass, methods)

    def _function(self, kind: str) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, f"Expected {kind} name")
        self._consume(TokenType.LEFT_PAREN, f"Expected ( after {kind} name")

        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            first_loop = True
            while first_loop or self._match(TokenType.COMMA):
                if len(arguments) > _MAX_NUM_ARGS:
                    self._error(
                        self._peek(), f"Can't have more than {_MAX_NUM_ARGS} arguments"
                    )
                arguments.append(
                    self._consume(TokenType.IDENTIFIER, "Expected parameter name")
                )

                first_loop = False

        self._consume(
            TokenType.RIGHT_PAREN, "Expected closing ) after function parameters"
        )
        self._consume(TokenType.LEFT_BRACE, f"Expected {'{'} before {kind} body")
        body = self._block()
        return Fun(name, arguments, body)

    def _var_declaration(self) -> Stmt:
        name = self._consume(TokenType.IDENTIFIER, "Expected variabled name.")

        initializer = None
        if self._match(TokenType.EQUAL):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return Var(name, initializer)

    def _statement(self) -> Stmt:

        if self._match(TokenType.FOR):
            return self._for_statement()

        if self._match(TokenType.IF):
            return self._if_statement()

        if self._match(TokenType.PRINT):
            return self._print_statement()

        if self._match(TokenType.RETURN):
            return self._return_statement()

        if self._match(TokenType.WHILE):
            return self._while_statement()

        if self._match(TokenType.LEFT_BRACE):
            return Block(self._block())

        return self._expression_statement()

    def _for_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expected ( after for")

        initializer = None
        if self._match(TokenType.SEMICOLON):
            pass
        elif self._match(TokenType.VAR):
            initializer = self._var_declaration()
        else:
            initializer = self._expression_statement()

        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ; after for condition")

        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ) after for clauses")

        body = self._statement()
        if increment != None:
            body = Block([body, Expression(increment)])

        if condition == None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer != None:
            body = Block([initializer, body])

        return body

    def _if_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expected ( after if")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ) after if condition")

        then_branch = self._statement()
        else_branch = self._statement() if self._match(TokenType.ELSE) else None
        return If(condition, then_branch, else_branch)

    def _while_statement(self) -> Stmt:
        self._consume(TokenType.LEFT_PAREN, "Expected ( after while")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expected ) after while condition")

        body = self._statement()
        return While(condition, body)

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

    def _return_statement(self) -> Stmt:
        keyword = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()

        self._consume(TokenType.SEMICOLON, "Expected ';' after return value")
        return Return(keyword, value)

    def _expression_statement(self) -> Stmt:
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return Expression(value)

    def _expression(self) -> Expr:
        return self._assignment()

    def _assignment(self) -> Expr:
        expr = self._or()
        if self._match(TokenType.EQUAL):
            equals = self._previous()
            value = self._assignment()

            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            elif type(expr) == Get:
                return Set(expr.obj, expr.name, value)

            raise self._error(equals, "Invalid assignment")
        return expr

    def _or(self) -> Expr:
        return self._match_left_associate_logical(self._and, TokenType.OR)

    def _and(self) -> Expr:
        return self._match_left_associate_logical(self._equality, TokenType.AND)

    def _match_left_associate_logical(
        self, operand_method: FunctionType, *types: TokenType
    ):
        expr = operand_method()

        while self._match(*types):
            operator = self._previous()
            right = operand_method()
            expr = Logical(expr, operator, right)

        return expr

    def _equality(self) -> Expr:
        return self._match_left_associate_binary(
            self._comparison, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL
        )

    def _match_left_associate_binary(
        self, operand_method: FunctionType, *types: TokenType
    ):
        expr = operand_method()

        while self._match(*types):
            operator = self._previous()
            right = operand_method()
            expr = Binary(expr, operator, right)

        return expr

    def _comparison(self) -> Expr:
        return self._match_left_associate_binary(
            self._term,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        )

    def _term(self) -> Expr:
        return self._match_left_associate_binary(
            self._factor, TokenType.MINUS, TokenType.PLUS
        )

    def _factor(self) -> Expr:
        return self._match_left_associate_binary(
            self._unary, TokenType.SLASH, TokenType.STAR
        )

    def _unary(self) -> Expr:
        if self._match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self._unary()
            return Unary(operator, right)

        return self._call()

    def _call(self) -> Expr:
        expr = self._primary()
        while True:
            if self._match(TokenType.LEFT_PAREN):
                expr = self._finish_call(expr)
            elif self._match(TokenType.DOT):
                name = self._consume(
                    TokenType.IDENTIFIER, "Expected property named after ."
                )
                expr = Get(expr, name)
            else:
                break

        return expr

    def _finish_call(self, callee: Expr) -> Expr:
        arguments: list[Expr] = []
        if not self._check(TokenType.RIGHT_PAREN):
            on_first_loop = True
            while on_first_loop or self._match(TokenType.COMMA):
                if len(arguments) > _MAX_NUM_ARGS:
                    self._error(
                        self._peek(), f"Can't have more than {_MAX_NUM_ARGS} arguments"
                    )
                arguments.append(self._expression())
                on_first_loop = False

        paren = self._consume(
            TokenType.RIGHT_PAREN, "Expected closing ) after function call"
        )

        return Call(callee, paren, arguments)

    def _primary(self) -> Expr:
        if self._match(TokenType.FALSE):
            return Literal(False)
        if self._match(TokenType.TRUE):
            return Literal(True)
        if self._match(TokenType.NIL):
            return Literal(None)

        if self._match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self._previous().value)

        if self._match(TokenType.SUPER):
            name = self._previous()
            self._consume(TokenType.DOT, "Expected '.' after 'super'.")
            method = self._consume(
                TokenType.IDENTIFIER, "Expected superclass method name"
            )
            return Super(name, method)

        if self._match(TokenType.THIS):
            return This(self._previous())

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous())

        if self._match(TokenType.LEFT_PAREN):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)

        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, type: TokenType, err_msg: str) -> Token:
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
