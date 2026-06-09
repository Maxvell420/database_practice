import requests
from .responses.response import Response
from .enums.result import Result
from .responses.LongPollServerResponse import LongPollServerResponse
from src.libs.infra.logger import Logger
class Client:

    API_URL = 'https://api.vk.com/method/'
    VK_API_VERSION = '5.199'

    def __init__(self, token: str, group_id: int, logger: Logger | None = None):
        self.token = token
        self.group_id = group_id
        # long poll server data может быть хранить в другом месте
        self._server :str | None = None
        self._key :str | None = None
        self._ts :str | None = None
        self._logger : Logger | None = logger

    @property
    def server(self) -> str | None:

        if self._server is None:
            self._server = self.getLognPollServer().server
        return self._server

    @property
    def key(self) -> str | None:
        if self._key is None:
            self._key = self.getLognPollServer().key
        return self._key

    @property
    def ts(self) -> str | None:
        if self._ts is None:
            self._ts = self.getLognPollServer().ts
        return self._ts

    def getLognPollServer(self) -> LongPollServerResponse:
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        data = {
            'group_id': self.group_id,
            'v': self.VK_API_VERSION
        }

        response = self.sendPostRequest(self.API_URL + 'groups.getLongPollServer', headers, data=data)

        if(not response.isOk()):
            raise Exception(response.data)
        return response.getLongPollServerResponse()

    def sendGetRequest(self, url: str, headers: dict, params: dict) -> Response:
        response = requests.get(url, headers=headers, params=params)

        if self._logger is not None:
            self._logger.info("Method: GET url: " + url + " params: " + str(params) + " response: " + str(response.text))

        status = Result.SUCCESS
        if response.status_code != 200:
            status = Result.ERROR
        return Response(status, response.json())

    #TODO передавать ts в метод
    def getUpdates(self) -> Response:
        server = self.server
        key = self.key
        ts = self.ts
        url = f"{server}?act=a_check&key={key}&ts={ts}&wait=25"
        # TODO параметры передавать напрямую а не конкатенацией
        response = self.sendGetRequest(url, {}, {})

        if(response.isOk()):
            self._ts = response.data['ts']
        return response

    def sendPostRequest(self, url: str, headers: dict, data: dict) -> Response:
        response = requests.post(url, headers=headers, data=data)
        status = Result.SUCCESS
        if response.status_code != 200:
            status = Result.ERROR
        return Response(status, response.json())