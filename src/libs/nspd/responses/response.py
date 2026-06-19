from src.libs.nspd.enums.result import Result
from typing import Any
from src.libs.nspd.responses.GeoportalSearchDataResponse import GeoportalSearchDataResponse
class Response:
    def __init__(self, result: Result, data: Any):
        self.result = result
        self.data : Any = data

    def isOk(self) -> bool:
        return self.result == Result.SUCCESS

    def getGeoportalSearchResponse(self) -> GeoportalSearchDataResponse:
        return GeoportalSearchDataResponse.model_validate(self.data)
