from typing import Any
from lox_token import Token


class Environment:
    _values: dict[str, Any]
    _enclosing: "Environment"

    def __init__(self, enclosing: "Environment" = None) -> None:
        self._values = dict()
        self._enclosing = enclosing

    def define(self, name: str, val: Any):
        self._values[name] = val

    def get(self, name: str) -> Any:
        if name in self._values:
            return self._values[name]

        if self._enclosing != None:
            return self._enclosing.get(name)

        raise Exception("PUT IN A RUNTIME EXCEPTION")

    def assign(self, name: str, val: Any) -> Any:
        if name in self._values:
            self._values[name] = val
            return

        if self._enclosing != None:
            self._enclosing.assign(name, val)
            return

        raise Exception("PUT IN A RUNTIME EXCEPTION")
