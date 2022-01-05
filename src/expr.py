import abc
from typing import Any
from dataclasses import dataclass
from lox_token import Token


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


class Expr(abc.ABC):
    # TODO: See if there's a cleaner way to do this, possibly with a @Visitor decorator on the Visitor class?
    @abc.abstractmethod
    def accept(self, visitor: ExprVisitor) -> Any:
        pass


@dataclass
class Assign(Expr):
    name: Token
    value: Expr

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
    callee: Expr
    paren: Token
    arguments: list[Expr]

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_call_expr(self)


@dataclass
class Get(Expr):
    obj: Expr
    name: Token

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
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_logical_expr(self)


@dataclass
class Set(Expr):
    object: Expr
    name: Token
    value: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_set_expr(self)


@dataclass
class Super(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_super_expr(self)


@dataclass
class This(Expr):
    name: Token

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
    name: Token

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_variable_expr(self)
