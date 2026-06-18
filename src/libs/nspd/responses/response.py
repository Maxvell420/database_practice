from src.libs.nspd.enums.result import Result
from typing import Any

class Response:
    def __init__(self, result: Result, data: Any):
        self.result = result
        self.data : Any = data

    def isOk(self) -> bool:
        return self.result == Result.SUCCESS
