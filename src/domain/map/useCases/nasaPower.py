from src.domain.map.repositories.nasaPowerRepository import NasaPowerRepository
from src.libs.nasapower.client import Client as NasapowerClient
import datetime
import pygeohash


class NasaPower:
    def __init__(
        self, repository: NasaPowerRepository, nasapowerClient: NasapowerClient
    ):
        self.repository = repository
        self.nasapowerClient = nasapowerClient

    def getByGeohashAndDate(self, latitude: float, longitude: float, time: float):
        geohash = pygeohash.encode(latitude, longitude, 5)
        geohashId = self.repository.findGeohashId(geohash)
        data = None

        if not geohashId:
            geohashId = self.repository.createGeohash(geohash)
        else:
            data = self.repository.getByGeohashAndDate(geohash, time)

        # Тут нужно подумать о том чтобы обновлять записи так как время идет..
        if not data:
            curdate = datetime.datetime.fromtimestamp(time)
            start_year_timestamp = curdate.replace(year=curdate.year, month=1, day=1)
            end_year_timestamp = curdate.replace(year=curdate.year, month=12, day=31)
            start_year_str = start_year_timestamp.strftime("%Y%m%d")
            end_str = end_year_timestamp.strftime("%Y%m%d")
            data = self.nasapowerClient.getDataByPointDaily(
                start_year_str, end_str, latitude, longitude
            )
            # Не совсем понял что значит community, пока так, потом переделать!
            self.repository.saveNasaPowerData(
                geohashId,
                data.getAllskySfcSwDwn(),
                int(start_year_timestamp.timestamp()),
                int(end_year_timestamp.timestamp()),
                "RE",
            )

        return data
