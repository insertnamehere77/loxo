import abc
from result import Result
from typing import Any
from dataclasses import dataclass
from lox_token import Token, TokenType


class ExprVisitor(abc.ABC):
    @abc.abstractmethod
    def visit_assign_expr(self, expr: "Assign") -> Any:
        pass

    @abc.abstractmethod
    def visit_binary_expr(self, expr: "Binary") -> Any:
        pass

    @abc.abstractmethod
    def visit_call_expr(self, expr: "Call") -> Any:
        pass

    @abc.abstractmethod
    def visit_get_expr(self, expr: "Get") -> Any:
        pass

    @abc.abstractmethod
    def visit_grouping_expr(self, expr: "Grouping") -> Any:
        pass

    @abc.abstractmethod
    def visit_literal_expr(self, expr: "Literal") -> Any:
        pass

    @abc.abstractmethod
    def visit_logical_expr(self, expr: "Logical") -> Any:
        pass

    @abc.abstractmethod
    def visit_set_expr(self, expr: "Set") -> Any:
        pass

    @abc.abstractmethod
    def visit_super_expr(self, expr: "Super") -> Any:
        pass

    @abc.abstractmethod
    def visit_this_expr(self, expr: "This") -> Any:
        pass

    @abc.abstractmethod
    def visit_unary_expr(self, expr: "Unary") -> Any:
        pass

    @abc.abstractmethod
    def visit_variable_expr(self, expr: "Variable") -> Any:
        pass


class ASTPrinter(ExprVisitor):
    def make_str(self, expr: "Expr") -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, *exprs: "Expr") -> str:
        str_exprs = " ".join([str(x.accept(self)) for x in exprs])
        return f"({name} {str_exprs})"

    def visit_assign_expr(self, expr: "Assign") -> str:
        print("Implement me please!")

    def visit_binary_expr(self, expr: "Binary") -> str:
        return self._parenthesize(expr.operator.token_type.value, expr.left, expr.right)

    def visit_call_expr(self, expr: "Call") -> str:
        print("Implement me please!")

    def visit_get_expr(self, expr: "Get") -> str:
        print("Implement me please!")

    def visit_grouping_expr(self, expr: "Grouping") -> str:
        return self._parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: "Literal") -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_logical_expr(self, expr: "Logical") -> str:
        print("Implement me please!")

    def visit_set_expr(self, expr: "Set") -> str:
        print("Implement me please!")

    def visit_super_expr(self, expr: "Super") -> str:
        print("Implement me please!")

    def visit_this_expr(self, expr: "This") -> str:
        print("Implement me please!")

    def visit_unary_expr(self, expr: "Unary") -> str:
        return self._parenthesize(expr.operator.token_type.value, expr.right)

    def visit_variable_expr(self, expr: "Variable") -> str:
        print("Implement me please!")


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
        self.message = f'Cannot apply operator {operator.value} tn value(s) {",".join(str(values))}'


class Interpreter(ExprVisitor):
    def interpret(self, expr: "Expr") -> Result[Any, LoxRuntimeError]:
        try:
            return Result.Ok(self.evaluate(expr))
        except (LoxRuntimeError, InvalidOperatorError) as err:
            return Result.Fail(err)

    def evaluate(self, expr: "Expr") -> Any:
        return expr.accept(self)

    def visit_assign_expr(self, expr: "Assign") -> Any:
        print("Implement me please!")

    def visit_binary_expr(self, expr: "Binary") -> Any:
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
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
        return self.evaluate(expr.expression)

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
        right = self.evaluate(expr.right)
        op_type = expr.operator.token_type

        if op_type == TokenType.MINUS:
            self._check_num_operands(expr.operator, right)
            return -right
        if op_type == TokenType.BANG:
            return not right

        raise InvalidOperatorError(op_type, right)

    def visit_variable_expr(self, expr: "Variable") -> Any:
        print("Implement me please!")

    def _check_num_operands(self, operator: Token, *operands: Any):
        not_nums = [num for num in operands if not isinstance(num, float)]

        if len(not_nums) > 0:
            raise LoxRuntimeError()


class Expr(abc.ABC):
    # TODO: See if there's a cleaner way to do this, possibly with a @Visitor decorator on the Visitor class?
    @abc.abstractmethod
    def accept(self, visitor: ExprVisitor) -> Any:
        pass


@dataclass
class Assign(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_assign_expr(self)


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_binary_expr(self)


@dataclass
class Call(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_call_expr(self)


@dataclass
class Get(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_get_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_literal_expr(self)


@dataclass
class Logical(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_logical_expr(self)


@dataclass
class Set(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_set_expr(self)


@dataclass
class Super(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_super_expr(self)


@dataclass
class This(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_this_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_unary_expr(self)


@dataclass
class Variable(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_variable_expr(self)
