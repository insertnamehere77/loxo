from environment import Environment
from result import Result
from typing import Any
from expr import (
    ExprVisitor,
    Expr,
    Assign,
    Binary,
    Unary,
    Call,
    Get,
    Grouping,
    Literal,
    Logical,
    Set,
    Super,
    This,
    Variable,
)
from stmt import StmtVisitor, Expression, Print, Stmt, Var, Block
from lox_token import Token, TokenType


class LoxRuntimeError(Exception):
    pass


class InvalidOperatorError(Exception):
    operator: TokenType
    values: tuple[Any]
    message: str

    def __init__(self, operator: TokenType, *values: Any) -> None:
        super().__init__()
        self.operator = operator
        self.values = values
        self.message = f'Cannot apply operator {operator.value} to value(s) {",".join(str(values))}'


class Interpreter(ExprVisitor, StmtVisitor):
    _env: Environment

    def __init__(self) -> None:
        super().__init__()
        self._env = Environment()

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except (LoxRuntimeError, InvalidOperatorError) as err:
            print("HEY DUDE THIS IS WHERE YOU LEFT OFF")

    def execute(self, statement: Stmt):
        statement.accept(self)

    def _evaluate(self, expr: "Expr") -> Any:
        return expr.accept(self)

    def visit_assign_expr(self, expr: "Assign") -> Any:
        value = self._evaluate(expr.value)
        self._env.assign(expr.name.value, value)
        return value

    def visit_binary_expr(self, expr: "Binary") -> Any:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        op_type = expr.operator.token_type

        # Arithmetic
        if op_type == TokenType.PLUS:
            if (type(left) == type(right)) and (
                isinstance(left, str) or isinstance(left, float)
            ):
                return left + right
            raise LoxRuntimeError()
        if op_type == TokenType.MINUS:
            self._check_num_operands(expr.operator, left, right)
            return left - right
        if op_type == TokenType.STAR:
            self._check_num_operands(expr.operator, left, right)
            return left * right
        if op_type == TokenType.SLASH:
            self._check_num_operands(expr.operator, left, right)
            return left / right

        # Comparison
        if op_type == TokenType.EQUAL_EQUAL:
            return left == right
        if op_type == TokenType.BANG_EQUAL:
            return left != right
        if op_type == TokenType.GREATER:
            self._check_num_operands(expr.operator, left, right)
            return left > right
        if op_type == TokenType.GREATER_EQUAL:
            self._check_num_operands(expr.operator, left, right)
            return left >= right
        if op_type == TokenType.LESS:
            self._check_num_operands(expr.operator, left, right)
            return left < right
        if op_type == TokenType.LESS_EQUAL:
            self._check_num_operands(expr.operator, left, right)
            return left <= right

        raise InvalidOperatorError(op_type, left, right)

    def visit_call_expr(self, expr: "Call") -> Any:
        print("Implement me please!")

    def visit_get_expr(self, expr: "Get") -> Any:
        print("Implement me please!")

    def visit_grouping_expr(self, expr: "Grouping") -> Any:
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: "Literal") -> Any:
        return expr.value

    def visit_logical_expr(self, expr: "Logical") -> Any:
        print("Implement me please!")

    def visit_set_expr(self, expr: "Set") -> Any:
        print("Implement me please!")

    def visit_super_expr(self, expr: "Super") -> Any:
        print("Implement me please!")

    def visit_this_expr(self, expr: "This") -> Any:
        print("Implement me please!")

    def visit_unary_expr(self, expr: "Unary") -> Any:
        right = self._evaluate(expr.right)
        op_type = expr.operator.token_type

        if op_type == TokenType.MINUS:
            self._check_num_operands(expr.operator, right)
            return -right
        if op_type == TokenType.BANG:
            return not right

        raise InvalidOperatorError(op_type, right)

    def visit_variable_expr(self, expr: "Variable") -> Any:
        return self._env.get(expr.name.value)

    def _check_num_operands(self, operator: Token, *operands: Any):
        not_nums = [num for num in operands if not isinstance(num, float)]

        if len(not_nums) > 0:
            raise LoxRuntimeError()

    # Stmt

    def visit_expression_stmt(self, stmt: "Expression") -> None:
        self._evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: "Print") -> None:
        val = self._evaluate(stmt.expression)
        print(val)

    def visit_var_stmt(self, stmt: "Var") -> None:
        val = None
        if stmt.initializer != None:
            val = self._evaluate(stmt.initializer)

        self._env.define(stmt.name.value, val)

    def visit_block_stmt(self, stmt: "Block") -> None:
        self._execute_block(stmt.statements, Environment(self._env))

    def _execute_block(self, statements: list[Stmt], env: Environment) -> None:

        prev = self._env
        try:
            self._env = env
            for statement in statements:
                self.execute(statement)
        finally:
            self._env = prev
