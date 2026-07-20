from src.libs.vk.enums.result import Result
from typing import Any
from .LongPollServerResponse import LongPollServerResponse
from .sendMessageDataResponse import SendMessageDataResponse
from .update import Update


class Response:
    def __init__(self, result: Result, data: Any):
        self.result = result
        self.data: Any = data

    def isOk(self) -> bool:
        return self.result == Result.SUCCESS

    # Переделать на pydantic
    def getLongPollServerResponse(self) -> LongPollServerResponse:
        return LongPollServerResponse(
            self.data["response"]["server"],
            self.data["response"]["key"],
            self.data["response"]["ts"],
        )

    def getUpdatesResponse(self) -> list[Update]:
        data = []
        for update in self.data["updates"]:
            data.append(Update.model_validate(update))
        return data

    def getSendMessageDataResponse(self) -> SendMessageDataResponse:
        return SendMessageDataResponse.model_validate(self.data)
