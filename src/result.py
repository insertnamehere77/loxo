from typing import Any, TypeVar, Generic


ValType = TypeVar("ValType")
ErrType = TypeVar("ErrType")


class Result(Generic[ValType, ErrType]):
    success: bool
    _result: Any

    def __init__(self, success: bool, result: Any) -> None:
        self.success = success
        self._result = result

    def __repr__(self) -> str:
        if self.success:
            return "<Result.success: {}>".format(self._result)

        return "<Result.failure: {}>".format(self._result)

    @property
    def failure(self) -> bool:
        return not self.success

    @property
    def value(self) -> ValType:
        return self._result if (self.success) else None

    @property
    def error(self) -> ErrType:
        return self._result if (not self.success) else None

    @classmethod
    def Ok(cls, val: ValType) -> "Result[ValType, ErrType]":
        return cls(success=True, result=val)

    @classmethod
    def Fail(cls, err: ErrType) -> "Result[ValType, ErrType]":
        return cls(success=False, result=err)
