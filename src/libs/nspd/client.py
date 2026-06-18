import requests
from src.libs.infra.logger import Logger
from src.libs.nspd.responses.response import Response
from src.libs.nspd.enums.result import Result
class Client:
    API_URL = 'https://nspd.gov.ru/api/geoportal/v2'

    def __init__(self, logger: Logger):
        self.logger = logger

    def getGeoportalSearch(self, query: str) -> Response:
        url = f'{self.API_URL}/search/geoportal'
        params = {
            'query': query
        }
        self.logger.info(f'Getting geoportal search: {url} {params}')

        return self.sendGetRequest(url, params, False)

    def sendGetRequest(self, url: str, params: dict, verify: bool = False) -> Response:
        response = requests.get(url, params=params,verify=verify)
        if response.status_code != 200:
            self.logger.error(f'Error getting geoportal search: {response.status_code} {response.text}')
            return Response(Result.ERROR, response.text)
        return Response(Result.SUCCESS, response.json())