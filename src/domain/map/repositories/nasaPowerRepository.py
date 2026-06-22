from src.domain.map.values.nasaPowerPoint import NasaPowerPoint
from src.libs.infra.baseRepository import BaseRepository
from asyncpg.protocol.record import Record
from typing import Any, cast
import json
class NasaPowerRepository(BaseRepository):

    async def getByGeohashAndDate(self, geohash: str, timestamp: float) -> NasaPowerPoint | None:
        sql = """
            SELECT nasapower_geohashes_data.data
            FROM geohashes
            INNER JOIN nasapower_geohashes_data
                ON geohashes.id = nasapower_geohashes_data.geohash_id
            WHERE geohashes.geohash = $1
              AND nasapower_geohashes_data.timestamp_from <= $2
              AND nasapower_geohashes_data.timestamp_to >= $2
            ORDER BY timestamp_from ASC
            LIMIT 1
        """
        async with self.connection() as conn:
            row = await conn.fetchrow(sql, geohash, timestamp)
            if row is None:
                return None
            data = json.loads(row.get('data'))
            return NasaPowerPoint(data=data)

    async def createGeohash(self, geohash: str) -> int:
        sql = """
            INSERT INTO geohashes (geohash) VALUES ($1)
            ON CONFLICT (geohash) DO NOTHING
            RETURNING id
        """
        async with self.connection() as conn:
            geohash_id = await conn.fetchval(sql, geohash)

        if geohash_id is None:
            raise Exception("Failed to create geohash")

        return int(geohash_id)

    async def findGeohashId(self, geohash: str) -> int | None:
        sql = """
            SELECT id FROM geohashes WHERE geohash = $1
        """
        async with self.connection() as conn:
            geohash_id = await conn.fetchval(sql, geohash)

        if geohash_id is None:
            return None

        return int(geohash_id)

    async def saveNasaPowerData(
        self,
        geohashId: int,
        data: dict[str, float],
        timestamp_from: int,
        timestamp_to: int,
        data_type: str,
    ) -> None:
        sql = """
            INSERT INTO nasapower_geohashes_data
                (geohash_id, data_type, timestamp_from, timestamp_to, data)
            VALUES ($1, $2, $3, $4, $5)
        """
        async with self.connection() as conn:
            await conn.execute(
                sql, geohashId, data_type, timestamp_from, timestamp_to, data
            )
