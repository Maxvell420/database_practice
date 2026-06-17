from src.libs.nasapower.enums.result import Result
from typing import Any
from src.libs.nasapower.responses.allskyDaily import AllskyDaily
class Response:
    def __init__(self, result: Result, data: Any):
        self.result = result
        self.data : Any = data

    def isOk(self) -> bool:
        return self.result == Result.SUCCESS

    def getAllskyDaily(self) -> AllskyDaily:
        return AllskyDaily.model_validate_json(self.data)