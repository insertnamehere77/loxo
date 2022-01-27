from os import name
from typing import Any
from lox_token import Token
from runtime_errors import LoxRuntimeError


class Environment:
    _values: dict[str, Any]
    _enclosing: "Environment"

    def __init__(self, enclosing: "Environment" = None) -> None:
        self._values = dict()
        self._enclosing = enclosing

    def define(self, name: str, val: Any):
        self._values[name] = val

    def get(self, name_token: Token) -> Any:
        name = name_token.value
        if name in self._values:
            return self._values[name]

        if self._enclosing != None:
            return self._enclosing.get(name_token)

        raise LoxRuntimeError(f"Variable {name} not found", name_token)

    def assign(self, name_token: Token, val: Any) -> Any:
        name = name_token.value
        if name in self._values:
            self._values[name] = val
            return

        if self._enclosing != None:
            self._enclosing.assign(name_token, val)
            return

        raise LoxRuntimeError(
            f"Variable {name} not initialized before assignment", name_token
        )

    def get_at(self, distance: int, name: str) -> Any:
        return self._ancestor(distance)._values.get(name)

    def assign_at(self, distance: int, name: str, value: Any) -> None:
        self._ancestor(distance)._values[name] = value

    def _ancestor(self, distance: int) -> "Environment":
        env: "Environment" = self
        for i in range(distance):
            env = env._enclosing

        return env
