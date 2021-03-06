from environment import Environment
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
from lox_token import Token, TokenType
from runtime_errors import LoxRuntimeError, InvalidOperatorError
import time, abc


class ReturnErr(Exception):
    value: Any

    def __init__(self, val: Any) -> None:
        super().__init__()
        self.value = val


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> Any:
        pass

    @abc.abstractmethod
    def arity(
        self,
    ) -> int:
        pass


class LoxFunction(LoxCallable):
    _declaration: Fun
    _closure: Environment
    _is_init: bool

    def __init__(
        self, declaration: Fun, closure: Environment, is_init: bool = False
    ) -> None:
        super().__init__()
        self._declaration = declaration
        self._closure = closure
        self._is_init = is_init

    def call(self, interpreter: "Interpreter", arguments: list[Any]):
        env = Environment(self._closure)
        for i in range(len(self._declaration.params)):
            param_name = self._declaration.params[i].value
            param_val = arguments[i]
            env.define(param_name, param_val)
        try:
            interpreter._execute_block(self._declaration.body, env)
        except ReturnErr as ret:
            if self._is_init:
                return self._closure.get_at(0, "this")
            return ret.value

        if self._is_init:
            return self._closure.get_at(0, "this")
        return None

    def arity(self) -> int:
        return len(self._declaration.params)

    def bind(self, instance: "LoxInstance"):
        env = Environment(self._closure)
        env.define("this", instance)
        return LoxFunction(self._declaration, env, self._is_init)


class ClockFn(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> float:
        return time.time()


# TODO: Maybe this should be a LoxRuntimeException?
class LoxAssertFailedError(Exception):
    line: int

    def __str__(self) -> str:
        return f"Line {self.line}: Assert failed!"


class AssertFn(LoxCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> float:
        if not arguments[0]:
            raise LoxAssertFailedError()


class AssertFalseFn(LoxCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> float:
        if arguments[0]:
            raise LoxAssertFailedError()


class LoxInstance:
    _class: "LoxRuntimeClass"
    _fields: dict

    def __init__(self, lox_class: "LoxRuntimeClass") -> None:
        self._class = lox_class
        self._fields = dict()

    def __str__(self) -> str:
        return self._class._name

    def get(self, name: Token):
        name_str = name.value
        if name_str in self._fields:
            return self._fields[name_str]

        method = self._class.find_method(name_str)
        if method != None:
            return method.bind(self)

        raise LoxRuntimeError(f"Undefined property: {name_str}.", name)

    def set(self, name: str, value: Any):
        self._fields[name] = value


class LoxRuntimeClass(LoxCallable):
    _name: str
    _superclass: "LoxRuntimeClass"
    _methods: dict

    def __init__(self, name, superclass: "LoxRuntimeClass", methods: dict) -> None:
        self._name = name
        self._superclass = superclass
        self._methods = methods

    def arity(self) -> int:
        initializer = self.find_method("init")
        if initializer != None:
            return initializer.arity()

        return 0

    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> Any:
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if initializer != None:
            initializer.bind(instance).call(interpreter, arguments)
        return instance

    def find_method(self, name: str) -> LoxFunction:
        if name in self._methods:
            return self._methods[name]

        if self._superclass != None:
            return self._superclass.find_method(name)


class Interpreter(ExprVisitor, StmtVisitor):
    _globals: Environment
    _env: Environment
    # The book has this as <Expr, int>
    # I think Token is probably fine for this with it's default hash method, but might need to revisit
    _locals: dict[Token, int]

    def __init__(self) -> None:
        super().__init__()
        self._globals = Environment()
        self._env = self._globals
        self._locals = dict()

        self._globals.define("clock", ClockFn())
        self._globals.define("assert", AssertFn())
        self._globals.define("assertFalse", AssertFalseFn())

    def interpret(self, statements: list[Stmt]):
        for statement in statements:
            self.execute(statement)

    def execute(self, statement: Stmt):
        statement.accept(self)

    def _evaluate(self, expr: "Expr") -> Any:
        return expr.accept(self)

    def visit_assign_expr(self, expr: "Assign") -> Any:
        value = self._evaluate(expr.value)

        distance = self._locals.get(expr.name)
        if distance != None:
            self._env.assign_at(distance, expr.name.value, value)
        else:
            self._globals.assign(expr.name, value)

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
            raise InvalidOperatorError(expr.operator, left, right)
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

        raise InvalidOperatorError(expr.operator, left, right)

    def visit_call_expr(self, expr: "Call") -> Any:
        callee = self._evaluate(expr.callee)

        arguments = [self._evaluate(arg) for arg in expr.arguments]

        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError("Can only call functions and classes", expr.paren)

        function: LoxCallable = callee

        if function.arity() != len(arguments):
            raise LoxRuntimeError(
                f"Wrong number of args, expected {function.arity()} but recieved {len(arguments)}",
                expr.paren,
            )
        try:
            return function.call(self, arguments)
        except (LoxAssertFailedError) as err:
            err.line = expr.paren.line
            raise err

    def visit_get_expr(self, expr: "Get") -> Any:
        obj = self._evaluate(expr.obj)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)

        raise LoxRuntimeError("Can only call propertes on objects", expr.name)

    def visit_grouping_expr(self, expr: "Grouping") -> Any:
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr: "Literal") -> Any:
        return expr.value

    def visit_logical_expr(self, expr: "Logical") -> Any:
        left_val = self._evaluate(expr.left)
        if expr.operator.token_type == TokenType.OR:
            if left_val:
                return left_val
        elif expr.operator.token_type == TokenType.AND:
            if not left_val:
                return left_val

        return self._evaluate(expr.right)

    def visit_set_expr(self, expr: "Set") -> Any:
        obj = self._evaluate(expr.object)
        if not type(obj) == LoxInstance:
            raise LoxRuntimeError("Only instances have fields", expr.name)

        val = self._evaluate(expr.value)
        obj.set(expr.name.value, val)
        return val

    def visit_super_expr(self, expr: "Super") -> Any:
        dist = self._locals.get(expr.name)
        superclass: LoxRuntimeClass = self._env.get_at(dist, "super")
        obj = self._env.get_at(dist - 1, "this")

        method = superclass.find_method(expr.method.value)
        if method == None:
            raise LoxRuntimeError(f"Undefined property {expr.method.value}", expr.name)
        return method.bind(obj)

    def visit_this_expr(self, expr: "This") -> Any:
        return self._lookup_variable(expr.name, expr)

    def visit_unary_expr(self, expr: "Unary") -> Any:
        right = self._evaluate(expr.right)
        op_type = expr.operator.token_type

        if op_type == TokenType.MINUS:
            self._check_num_operands(expr.operator, right)
            return -right
        if op_type == TokenType.BANG:
            return not right

        raise InvalidOperatorError(expr.operator, right)

    def visit_variable_expr(self, expr: "Variable") -> Any:
        return self._lookup_variable(expr.name, expr)

    def _lookup_variable(self, name: Token, expr: Variable):
        dist = self._locals.get(expr.name)
        if dist != None:
            return self._env.get_at(dist, name.value)

        return self._globals.get(name)

    def _check_num_operands(self, operator: Token, *operands: Any):
        not_nums = [num for num in operands if not isinstance(num, float)]

        if len(not_nums) > 0:
            raise InvalidOperatorError(operator, *operands)

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

    def visit_if_stmt(self, stmt: "If") -> None:
        if self._evaluate(stmt.condition):
            self.execute(stmt.then_branch)
        elif stmt.else_branch != None:
            self.execute(stmt.else_branch)

    def visit_while_stmt(self, stmt: "While") -> Any:
        while self._evaluate(stmt.condition):
            self.execute(stmt.body)

    def visit_fun_stmt(self, stmt: "Fun") -> Any:
        func = LoxFunction(stmt, self._env)
        self._env.define(stmt.name.value, func)

    def visit_return_stmt(self, stmt: "Return") -> Any:
        value = None
        if stmt.value != None:
            value = self._evaluate(stmt.value)

        raise ReturnErr(value)

    def resolve(self, expr: Expr, depth: int) -> None:
        self._locals[expr.name] = depth

    def visit_class_stmt(self, stmt: "LoxClass") -> Any:

        superclass = None
        if stmt.superclass != None:
            superclass = self._evaluate(stmt.superclass)
            if type(superclass) != LoxRuntimeClass:
                raise LoxRuntimeError("Superclass must be a class.", stmt.name)

        self._env.define(stmt.name.value, None)

        if stmt.superclass != None:
            self._env = Environment(self._env)
            self._env.define("super", superclass)

        methods = dict()
        for method in stmt.methods:
            is_init = method.name.value == "init"
            func = LoxFunction(method, self._env, is_init)
            methods[method.name.value] = func

        klass = LoxRuntimeClass(stmt.name.value, superclass, methods)

        if superclass != None:
            self._env = self._env._enclosing

        self._env.assign(stmt.name, klass)
