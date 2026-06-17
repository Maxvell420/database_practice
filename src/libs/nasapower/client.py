import requests

from src.libs.infra.logger import Logger
from src.libs.nasapower.enums.community import Community
from src.libs.nasapower.enums.units import Units
from src.libs.nasapower.enums.timestandart import TimeStandard

class Client:

    API_URL = 'https://power.larc.nasa.gov/api'
    
    def __init__(self, logger: Logger):
        self.logger = logger


    def getDataByPointHourly(self, start_date: str, end_date: str, latitude: float, longitude: float, units: Units = Units.METRIC, user: str = 'DAVE', time_standard: TimeStandard = TimeStandard.LST):
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

        self.logger.info(f'Getting data by point hourly: {url} {params}')
        response = requests.get(url, params=params)
        self.logger.info('Response: ' + str(response.text))
        return response.json()