from src.libs.vk.enums.result import Result
from typing import Any
from .LongPollServerResponse import LongPollServerResponse
from .updatesResponse import UpdatesResponse
from src.libs.vk.enums.updateType import UpdateType
class Response:
    def __init__(self, result: Result, data: Any):
        self.result = result
        self.data : Any = data

    def isOk(self) -> bool:
        return self.result == Result.SUCCESS

    def getLongPollServerResponse(self) -> LongPollServerResponse:
        return LongPollServerResponse(self.data['response']['server'], self.data['response']['key'], self.data['response']['ts'])

    # def getUpdatesResponse(self) -> UpdatesResponse:

    #     for update in self.data['response']['updates']:
    #         if update['type'] == UpdateType.MESSAGE_NEW:
    #     return UpdatesResponse(self.data['response']['updates'], self.data['response']['ts'])