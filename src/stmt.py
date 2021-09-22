import abc
from lox_token import Token
from expr import Expr
from typing import Any
from dataclasses import dataclass


class StmtVisitor(abc.ABC):
    @abc.abstractmethod
    def visit_expression_stmt(self, stmt: "Expression") -> Any:
        pass

    @abc.abstractmethod
    def visit_print_stmt(self, stmt: "Print") -> Any:
        pass

    @abc.abstractmethod
    def visit_var_stmt(self, stmt: "Var") -> Any:
        pass

    @abc.abstractmethod
    def visit_block_stmt(self, stmt: "Var") -> Any:
        pass


class Stmt(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: StmtVisitor) -> Any:
        pass


@dataclass
class Expression(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_print_stmt(self)


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_var_stmt(self)


@dataclass
class Block(abc.ABC):
    statements: list[Stmt]

    def accept(self, visitor: StmtVisitor) -> Any:
        return visitor.visit_block_stmt(self)
