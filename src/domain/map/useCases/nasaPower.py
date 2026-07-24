from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.domain.map.values.nasaPowerPoint import NasaPowerPoint
from src.libs.nasapower.client import Client as NasapowerClient
import datetime
import pygeohash


class NasaPower:
    def __init__(
        self, repository: NasaPowerRepository, nasapowerClient: NasapowerClient
    ):
        self.repository = repository
        self.nasapowerClient = nasapowerClient

    async def getRadiationByCoordinates(
        self, latitude: float, longitude: float, time: float
    ) -> NasaPowerPoint:
        geohash = pygeohash.encode(latitude, longitude, 5)
        geohashId = await self.repository.findGeohashId(geohash)
        data = None

        if not geohashId:
            geohashId = await self.repository.createGeohash(geohash)
        else:
            data = await self.repository.findByGeohashAndDate(geohash, time)

        # Тут нужно подумать о том чтобы обновлять записи так как время идет..
        if not data:
            curdate = datetime.datetime.fromtimestamp(time)
            start_year_timestamp = curdate.replace(year=curdate.year, month=1, day=1)
            end_year_timestamp = curdate.replace(year=curdate.year, month=12, day=31)
            start_year_str = start_year_timestamp.strftime("%Y%m%d")
            end_str = end_year_timestamp.strftime("%Y%m%d")
            allskyDaily = await self.nasapowerClient.getDataByPointDaily(
                start_year_str, end_str, latitude, longitude
            )
            allskyData = allskyDaily.getAllskySfcSwDwn()
            # Не совсем понял что значит community, пока так, потом переделать!
            await self.repository.saveNasaPowerData(
                geohashId,
                allskyData,
                int(start_year_timestamp.timestamp()),
                int(end_year_timestamp.timestamp()),
                "RE",
            )
            data = NasaPowerPoint(data=allskyData)

        return data
