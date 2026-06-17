from src.libs.infra.baseRepository import BaseRepository
from src.domain.map.values.nasaYearPower import NasaYearPower
from datetime import datetime
class NasaPowerRepository(BaseRepository):

    def getByGeohashAndDate(self, geohash: str, timestamp: float):
        sql = f"""
            SELECT 
                * 
            FROM 
                geohashes
            INNER JOIN nasapower_geohashes_data ON (geohashes.id = nasapower_geohashes_data.geohash_id)
            WHERE 
                geohashes.geohash = '{geohash}' 
                AND nasapower_geohashes_data.timestamp_from <= {timestamp} 
                AND nasapower_geohashes_data.timestamp_to >= {timestamp}
            ORDER BY 
                timestamp_from ASC
        """

        db = self.db.cursor()
        db.execute(sql)
        data = []
        while row := db.fetchone():

            print(row)
            # data.append(NasaYearPower(
            #     year=row[0],
            #     data=row[1]
            # ))

        return data
