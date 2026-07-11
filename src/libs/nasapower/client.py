import requests_async

from src.libs.infra.logger import Logger
from src.libs.nasapower.enums.community import Community
from src.libs.nasapower.enums.units import Units
from src.libs.nasapower.enums.timestandart import TimeStandard
from src.libs.nasapower.enums.result import Result
from src.libs.nasapower.responses.response import Response
from src.libs.nasapower.responses.allskyDaily import AllskyDaily
class Client:

    API_URL = 'https://power.larc.nasa.gov/api'
    
    def __init__(self, logger: Logger):
        self.logger = logger


    async def getDataByPointDaily(self, start_date: str, end_date: str, latitude: float, longitude: float, units: Units = Units.METRIC, user: str = 'DAVE', time_standard: TimeStandard = TimeStandard.LST) -> AllskyDaily:
        url = f'{self.API_URL}/temporal/daily/point'
        params = {
            'start': start_date,
            'end': end_date,
            'latitude': latitude,
            'longitude': longitude,
            'community': Community.RE.value,
            'units': units.value,
            'parameters': 'ALLSKY_SFC_SW_DWN',
            'format': 'JSON',
        }

        response =await self.sendGetRequest(url, params)
        if not response.isOk():
            # подумать че делать, мб сделать исключение для либы специальное
            # по какой-то неведомой причине для обычных людей в начале lat потом long, а в ответе апи long,lat,altitude
            raise Exception('Failed to get data by point daily')
        return response.getAllskyDaily()

    async def sendGetRequest(self, url: str, params: dict) -> Response:
        await self.logger.info(f'Getting data by point hourly: {url} {params}')
        response = await requests_async.get(url, params=params)
        status = Result.SUCCESS
        if response.status_code != 200:
            status = Result.ERROR
            await self.logger.error(f'Response: {response.text}')
        # не логирую ок запросы
        return Response(status, response.text)