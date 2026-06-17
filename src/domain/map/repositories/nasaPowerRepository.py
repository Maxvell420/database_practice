from src.libs.infra.baseRepository import BaseRepository
import json
from src.domain.map.values.nasaPowerPoint import NasaPowerPoint
class NasaPowerRepository(BaseRepository):

    def getByGeohashAndDate(self, geohash: str, timestamp: float) -> NasaPowerPoint | None:
        sql = f"""
            SELECT 
                nasapower_geohashes_data.data
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
        row = db.fetchone()
        if row:
            return NasaPowerPoint(
                data=row[0]
            )

        return None

    def createGeohash(self, geohash: str) -> int:
        sql = f"""
            INSERT INTO geohashes (geohash) VALUES ('{geohash}')
            ON CONFLICT (geohash) DO NOTHING
            RETURNING geohashes.id
        """
        db = self.db.cursor()
        db.execute(sql)
        self.db.commit()

        row = db.fetchone()
        if row:
            return int(row[0])
        else:
            raise Exception("Failed to create geohash")

    def findGeohashId(self, geohash: str) -> int | None:
        sql = f"""
            SELECT geohashes.id FROM geohashes WHERE geohashes.geohash = '{geohash}'
        """
        db = self.db.cursor()
        db.execute(sql)
        row = db.fetchone()
        if row:
            return int(row[0])
        else:
            return None


    def saveNasaPowerData(self, geohashId: int, data: dict[str, float], timestamp_from: int, timestamp_to: int, data_type: str):
        sql = f"""
            INSERT INTO nasapower_geohashes_data (geohash_id, data_type, timestamp_from, timestamp_to, data) VALUES ({geohashId}, '{data_type}', {timestamp_from}, {timestamp_to}, '{json.dumps(data)}')
        """
        db = self.db.cursor()
        db.execute(sql)
        self.db.commit()