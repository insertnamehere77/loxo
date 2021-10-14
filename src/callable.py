import abc
from typing import Any


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def call(self, interpreter: "Interpreter", arguments: list[Any]) -> Any:
        pass

    @abc.abstractmethod
    def arity(
        self,
    ) -> int:
        pass
