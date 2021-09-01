from typing import Any


# TODO: It would be nice to communicate what type the _result is as maybe a generic or something?


class Result:
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
    def value(self) -> Any:
        return self._result if (self.success) else None

    @property
    def error(self) -> Any:
        return self._result if (not self.success) else None

    @classmethod
    def Ok(cls, val: Any):
        return cls(success=True, result=val)

    @classmethod
    def Fail(cls, err: Any):
        return cls(success=False, result=err)
