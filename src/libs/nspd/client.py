import requests_async
from src.libs.infra.logger import Logger
from src.libs.nspd.responses.response import Response
from src.libs.nspd.enums.result import Result
from src.libs.nspd.responses.geoportalSearchResponse import GeoportalSearchResponse
class Client:
    API_URL = 'https://nspd.gov.ru/api/geoportal/v2'

    def __init__(self, logger: Logger):
        self.logger = logger

    async def getGeoportalSearch(self, query: str) -> GeoportalSearchResponse:
        url = f'{self.API_URL}/search/geoportal'
        params = {
            'query': query
        }
        self.logger.info(f'Getting geoportal search: {url} {params}')
        response = await self.sendGetRequest(url, params, False)
        if not response.isOk():
            raise Exception('Не удалось получить данные из API кадастровой карты')
            # Нужно распарсить ответ и если временный блок то еще раз?p
        return response.getGeoportalSearchResponse().data

    async def sendGetRequest(self, url: str, params: dict, verify: bool = False) -> Response:
        response = await requests_async.get(url, params=params,verify=verify,headers={'Referer': 'https://nspd.gov.ru/map?'})
        if response.status_code != 200:
            self.logger.error(f'Error getting geoportal search: {response.status_code} {response.text}')
            return Response(Result.ERROR, response.text)
        return Response(Result.SUCCESS, response.json())
