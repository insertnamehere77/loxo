import abc
from typing import Any
from dataclasses import dataclass
from lox_token import Token, TokenType


class ExprVisitor(abc.ABC):
    @abc.abstractmethod
    def visitAssignExpr(self, expr: "Assign") -> Any:
        pass

    @abc.abstractmethod
    def visitBinaryExpr(self, expr: "Binary") -> Any:
        pass

    @abc.abstractmethod
    def visitCallExpr(self, expr: "Call") -> Any:
        pass

    @abc.abstractmethod
    def visitGetExpr(self, expr: "Get") -> Any:
        pass

    @abc.abstractmethod
    def visitGroupingExpr(self, expr: "Grouping") -> Any:
        pass

    @abc.abstractmethod
    def visitLiteralExpr(self, expr: "Literal") -> Any:
        pass

    @abc.abstractmethod
    def visitLogicalExpr(self, expr: "Logical") -> Any:
        pass

    @abc.abstractmethod
    def visitSetExpr(self, expr: "Set") -> Any:
        pass

    @abc.abstractmethod
    def visitSuperExpr(self, expr: "Super") -> Any:
        pass

    @abc.abstractmethod
    def visitThisExpr(self, expr: "This") -> Any:
        pass

    @abc.abstractmethod
    def visitUnaryExpr(self, expr: "Unary") -> Any:
        pass

    @abc.abstractmethod
    def visitVariableExpr(self, expr: "Variable") -> Any:
        pass


class ASTPrinter(ExprVisitor):
    def make_str(self, expr: "Expr") -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, *exprs: "Expr") -> str:
        str_exprs = " ".join([str(x.accept(self)) for x in exprs])
        return f"({name} {str_exprs})"

    def visitAssignExpr(self, expr: "Assign") -> str:
        print("Implement me please!")

    def visitBinaryExpr(self, expr: "Binary") -> str:
        return self._parenthesize(expr.operator.token_type.value, expr.left, expr.right)

    def visitCallExpr(self, expr: "Call") -> str:
        print("Implement me please!")

    def visitGetExpr(self, expr: "Get") -> str:
        print("Implement me please!")

    def visitGroupingExpr(self, expr: "Grouping") -> str:
        return self._parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: "Literal") -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitLogicalExpr(self, expr: "Logical") -> str:
        print("Implement me please!")

    def visitSetExpr(self, expr: "Set") -> str:
        print("Implement me please!")

    def visitSuperExpr(self, expr: "Super") -> str:
        print("Implement me please!")

    def visitThisExpr(self, expr: "This") -> str:
        print("Implement me please!")

    def visitUnaryExpr(self, expr: "Unary") -> str:
        return self._parenthesize(expr.operator.token_type.value, expr.right)

    def visitVariableExpr(self, expr: "Variable") -> str:
        print("Implement me please!")


class Expr(abc.ABC):
    # TODO: See if there's a cleaner way to do this, possibly with a @Visitor decorator on the Visitor class?
    @abc.abstractmethod
    def accept(self, visitor: ExprVisitor) -> Any:
        pass


@dataclass
class Assign(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitAssignExpr(self)


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitBinaryExpr(self)


@dataclass
class Call(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitCallExpr(self)


@dataclass
class Get(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitGetExpr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitGroupingExpr(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitLiteralExpr(self)


@dataclass
class Logical(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitLogicalExpr(self)


@dataclass
class Set(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitSetExpr(self)


@dataclass
class Super(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitSuperExpr(self)


@dataclass
class This(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitThisExpr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitUnaryExpr(self)


@dataclass
class Variable(Expr):
    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visitVariableExpr(self)
