from src.libs.vk.enums.result import Result

class Response:
    def __init__(self, result: Result, data: dict | None = None):
        self.result = result
        self.data : dict | None = data

    def isOk(self) -> bool:
        return self.result == Result.SUCCESS