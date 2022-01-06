import enum
from lox_token import Token
from expr import (
    ExprVisitor,
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
from stmt import (
    StmtVisitor,
    Expression,
    Print,
    Stmt,
    Var,
    Block,
    If,
    While,
    Fun,
    Return,
    LoxClass,
)
from interpreter import Interpreter
from typing import Any


class LoxFunctionType(enum.Enum):
    NONE = enum.auto()
    FUNCTION = enum.auto()
    METHOD = enum.auto()
    INITIALIZER = enum.auto()


class LoxClassType(enum.Enum):
    NONE = enum.auto()
    CLASS = enum.auto()
    SUBCLASS = enum.auto()


class Resolver(ExprVisitor, StmtVisitor):
    _interpreter: Interpreter
    _scopes: list[dict]
    _currFunc: LoxFunctionType
    _currClass: LoxClassType

    def __init__(self, interpreter: Interpreter) -> None:
        super().__init__()
        self._interpreter = interpreter
        self._scopes = []
        self._currFunc = LoxFunctionType.NONE
        self._currClass = LoxClassType.NONE

    def visit_block_stmt(self, stmt: "Block") -> Any:
        self._begin_scope()
        self._resolve_stmts(stmt.statements)
        self._end_scope()

    def _begin_scope(self):
        self._scopes.append(dict())

    def _end_scope(self):
        self._scopes.pop()

    def _resolve_stmts(self, statements: list[Stmt]) -> None:
        for statement in statements:
            self._resolve(statement)

    # Stmt is either a Stmt or an Expr
    def _resolve(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def visit_var_stmt(self, stmt: Var) -> None:
        self._declare(stmt.name)
        if stmt.initializer != None:
            self._resolve(stmt.initializer)
        self._define(stmt.name)

    def _declare(self, name: Token) -> None:
        if len(self._scopes) == 0:
            return

        scope = self._scopes[-1]
        if name.value in scope:
            raise Exception("Already a variable with this name in this scope.")
        scope[name.value] = False

    def _define(self, name: Token) -> None:
        if len(self._scopes) == 0:
            return

        self._scopes[-1][name.value] = True

    def visit_variable_expr(self, expr: Variable) -> Any:
        if len(self._scopes) != 0 and self._scopes[-1].get(expr.name.value) == False:
            # TODO: Put in a more specific error
            raise Exception("Can't read local variable in its own initializer.")

        self._resolve_local(expr, expr.name)

    def _resolve_local(self, expr: Variable, name: Token) -> None:
        for i in range(len(self._scopes) - 1, -1, -1):
            if name.value in self._scopes[i]:
                self._interpreter.resolve(expr, len(self._scopes) - 1 - i)

    def visit_assign_expr(self, expr: Assign) -> None:
        self._resolve(expr.value)
        self._resolve_local(expr, expr.name)

    def visit_fun_stmt(self, stmt: Fun) -> None:
        self._declare(stmt.name)
        self._define(stmt.name)

        self._resolve_function(stmt, LoxFunctionType.FUNCTION)

    def _resolve_function(self, stmt: Fun, type: LoxFunctionType) -> None:
        enclosing = self._currFunc
        self._currFunc = type

        self._begin_scope()
        for param in stmt.params:
            self._declare(param)
            self._define(param)

        self._resolve_stmts(stmt.body)
        self._end_scope()
        self._currFunc = enclosing

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self._resolve(stmt.expression)

    def visit_if_stmt(self, stmt: If) -> Any:
        self._resolve(stmt.condition)
        self._resolve(stmt.then_branch)
        if stmt.else_branch != None:
            self._resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt: Print) -> Any:
        self._resolve(stmt.expression)

    def visit_return_stmt(self, stmt: Return) -> Any:
        if self._currFunc == LoxFunctionType.NONE:
            raise Exception("Can't return from top level code")

        if stmt.value != None:
            if self._currFunc == LoxFunctionType.INITIALIZER:
                raise Exception("Can't return a value from initializer")
            self._resolve(stmt.value)

    def visit_while_stmt(self, stmt: While) -> Any:
        self._resolve(stmt.condition)
        self._resolve(stmt.body)

    def visit_binary_expr(self, expr: "Binary") -> Any:
        self._resolve(expr.left)
        self._resolve(expr.right)

    def visit_call_expr(self, expr: "Call") -> Any:
        self._resolve(expr.callee)

        for arg in expr.arguments:
            self._resolve(arg)

    def visit_grouping_expr(self, expr: "Grouping") -> Any:
        self._resolve(expr.expression)

    def visit_literal_expr(self, expr: "Literal") -> Any:
        pass

    def visit_logical_expr(self, expr: "Logical") -> Any:
        self._resolve(expr.left)
        self._resolve(expr.right)

    def visit_unary_expr(self, expr: "Unary") -> Any:
        self._resolve(expr.right)

    def visit_class_stmt(self, stmt: "LoxClass") -> Any:
        enclosingClass = self._currClass
        self._currClass = LoxClassType.CLASS

        self._declare(stmt.name)
        self._define(stmt.name)

        if stmt.superclass != None and stmt.name.value == stmt.superclass.name.value:
            raise Exception("A class can't inherit from itself")

        if stmt.superclass != None:
            self._currClass = LoxClassType.SUBCLASS
            self._resolve(stmt.superclass)
            self._begin_scope()
            self._scopes[-1]["super"] = True

        self._begin_scope()
        self._scopes[-1]["this"] = True

        for method in stmt.methods:
            func_type = LoxFunctionType.METHOD
            if method.name.value == "init":
                func_type = LoxFunctionType.INITIALIZER
            self._resolve_function(method, func_type)

        self._end_scope()
        if stmt.superclass != None:
            self._end_scope()
        self._currClass = enclosingClass

    def visit_get_expr(self, expr: "Get") -> Any:
        self._resolve(expr.obj)

    def visit_set_expr(self, expr: "Set") -> Any:
        self._resolve(expr.value)
        self._resolve(expr.object)

    def visit_super_expr(self, expr: "Super") -> Any:
        if self._currClass != LoxClassType.SUBCLASS:
            raise Exception("Can't use super outside of a subclass")
        self._resolve_local(expr, expr.name)

    def visit_this_expr(self, expr: "This") -> Any:
        if self._currClass == LoxClassType.NONE:
            raise Exception("Can't use 'this' outside of a class.")
        self._resolve_local(expr, expr.name)
