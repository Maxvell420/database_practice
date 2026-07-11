import requests_async

from .responses.response import Response
from .enums.result import Result
from .responses.LongPollServerResponse import LongPollServerResponse
from src.libs.infra.logger import Logger
from .responses.update import Update
from .responses.sendMessageDataResponse import SendMessageDataResponse
from src.domain.messengers.vk.entities.inlineKeyboard import InlineKeyboard


class Client:

    API_URL = "https://api.vk.com/method/"
    VK_API_VERSION = "5.199"

    def __init__(self, token: str, group_id: int, logger: Logger | None = None):
        self.token = token
        self.group_id = group_id
        self.server: LongPollServerResponse | None = None
        self.logger: Logger | None = logger

    async def longPollServer(self) -> LongPollServerResponse:
        if self.server is None:
            self.server = await self.getLognPollServer()
        return self.server

    async def getLognPollServer(self) -> LongPollServerResponse:
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"group_id": self.group_id, "v": self.VK_API_VERSION}

        response = await self.sendPostRequest(
            self.API_URL + "groups.getLongPollServer", headers, data=data
        )

        if not response.isOk():
            raise Exception(response.data)
        return response.getLongPollServerResponse()

    async def sendGetRequest(self, url: str, headers: dict, params: dict) -> Response:
        response = await requests_async.get(url, headers=headers, params=params)

        if self.logger is not None:
            await self.logger.info(
                f"Method: GET url: {url} params: {params} response: {response.text}"
            )

        status = Result.SUCCESS
        if response.status_code != 200:
            status = Result.ERROR
        return Response(status, response.json())

    # TODO передавать ts в метод
    async def getUpdates(self) -> list[Update]:
        server = await self.longPollServer()
        key = server.key
        ts = server.ts
        url = server.server
        params = {"act": "a_check", "key": key, "ts": ts, "wait": 25}
        response = await self.sendGetRequest(url, {}, params)
        if response.isOk():
            server.ts = response.data["ts"]
        return response.getUpdatesResponse()

    async def sendPostRequest(self, url: str, headers: dict, data: dict) -> Response:

        if self.logger is not None:
            await self.logger.info(
                f"Method: POST url: {url} headers: {headers} data: {data}"
            )

        response = await requests_async.post(url, headers=headers, data=data)
        status = Result.SUCCESS
        if response.status_code != 200:
            status = Result.ERROR

        if self.logger is not None:
            await self.logger.info(
                f"Method: POST url: {url} headers: {headers} data: {data} response: {response.text}"
            )

        return Response(status, response.json())

    # TODO передавать обьект
    async def sendMessage(
        self, user_id: int, message: str, keyboard: InlineKeyboard | None = None
    ) -> SendMessageDataResponse:
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "message": message,
            "v": self.VK_API_VERSION,
            "user_id": user_id,
            "random_id": 0,
        }
        if keyboard is not None:
            data["keyboard"] = keyboard.model_dump_json(exclude_none=True)

        response = await self.sendPostRequest(
            self.API_URL + "messages.send", headers, data=data
        )

        if not (response.isOk()):
            raise Exception(response.data)

        return response.getSendMessageDataResponse()
